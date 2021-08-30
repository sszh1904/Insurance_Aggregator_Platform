from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pika

import paypalrestsdk
import logging
import webbrowser
import json
import urllib.parse
import os, sys

import amqp_setup
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

paypalrestsdk.configure({
    "mode":"sandbox",
    "client_id" : "<paypal_client_id>",
    "client_secret" : "<paypal_client_secret_key>"
})

policy_creation_url = os.environ.get('policy_creation_url') or "http://localhost:5000/createpolicy"
transaction_url = os.environ.get('transaction_url') or "http://localhost:5008/add_transaction"
customer_policy_url = os.environ.get('customer_policy_url') or "http://localhost:5002/add_cust_policy"

# Generate PayPal UI URL
@app.route("/payment", methods=["POST"])
def payment():
    print(request)
    # #retrieve all relevant fields
    result = request.get_json()
    print(result)
    user_id = request.json.get("nric") # "S9411494B"
    policy_id = request.json.get("policy_id") # "AIAWL2"
    policy_price = request.json.get("policy_price") # "5"
    customer_name = request.json.get("cust_name") # "Dave Low"
    customer_email = request.json.get("email") # "dave.low.2019@sis.smu.edu.sg"
    policy_name = request.json.get("policy_name") # "Blabla policy"
    params = {"userID":user_id, "policyID":policy_id, "policyName":policy_name, "policyPrice":policy_price, "customerName":customer_name, "customerEmail":customer_email}
    return_url = urllib.parse.urlencode(params)
    # return_url = "?userid={}&policyname={}".format(user_id,policy_name)
    print(return_url)

    payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost/Insurance_Aggregator/Insurance_Aggregator/templates/receipt.html?"+return_url,
        "cancel_url": "http://localhost/Insurance_Aggregator/Insurance_Aggregator/templates/policies.html"}, 
    "transactions": [{
        "item_list": {
            "items": [{
                "name": policy_name,#policyname
                "sku": policy_id, #policyID
                "price": policy_price, #policyPrice
                "currency": "SGD", 
                "quantity": 1}]},
        "amount": {
            "total": policy_price,
            "currency": "SGD"},
        "description": "This is the payment transaction description."}]})

    if payment.create():
        print(payment)
        links = payment["links"]

        approval_url = ""
        for link in links:
            if link["rel"]=="approval_url":
                approval_url = link["href"]
                print(approval_url)
                break
        
        if approval_url != "":
            return jsonify({"code": 200, "message": "Successful", "approval_URL": approval_url}), 200 # returns url to client for client to re-direct
        else:
            return jsonify({"code": 501, "message": "Unsuccessful from Paypal side"}), 501

    else:
        return jsonify({"code": 500, "message": "Unable to create payment object"}), 500


@app.route("/execute")
def execute():
    print("Routed to execute")
    success = False
    paymentID = request.args.get("paymentId")
    payerID = request.args.get("PayerID")
    userID = request.args.get("userID")
    policyID = request.args.get("policyID")
    policyName = request.args.get("policyName")
    policyPrice = request.args.get("policyPrice")
    customerName = request.args.get("customerName")
    customerEmail = request.args.get("customerEmail")
    payment = paypalrestsdk.Payment.find(paymentID)

    if payment.execute({"payer_id" : payerID}):
        print("executed")
        success= True
        receipt = {
            "success" : success,
            "customer_id": userID,
            "customer_name": customerName,
            "email": customerEmail,
            "policy_id": policyID,
            "policy_name": policyName,
            "price": payment["transactions"][0]["amount"]["total"],
            "paymentID": paymentID,
            "create_time": payment['create_time']
        }


        # Invoke 'Policy' microservice to create actual insurance policy with respective company
        print('\n------- Creating Actual insurance policy with company -------')
        policy_creation = invoke_http(policy_creation_url + "/" + policyID)
        print("Response: " + str(policy_creation))

        # Check for valid response - if invalid, return error. Else, append policy_creation details into receipt
        code = policy_creation["code"]

        if code not in range(200, 300):  
            print('\n-----Error with insurance API-----')  
            return jsonify(policy_creation), policy_creation['code']


        print('\n-----Aggregating Receipt and Policy Creation details-----')    
        receipt['policy_creation'] = policy_creation['data']

        print('\n... Done')
        
        
        
        # Record this transaction in the "Transaction" microservice
        filtered_receipt = {
            'trans_id': receipt['paymentID'],
            'cust_nric': receipt['customer_id'],
            'policy_creation_id': receipt['policy_creation']['policy_creation_id'],
            'trans_datetime': receipt['create_time'],
            'amount': receipt['price']
        }
        
        transaction_status = invoke_http(transaction_url, method='POST', json = filtered_receipt)
        print("Transaction record status:", transaction_status)

        # Check for valid response - if invalid, return error. 
        code = transaction_status["code"]

        if code not in range(200, 300):  
            print('\n-----Error with Transaction microservice-----')  
            return jsonify(transaction_status), transaction_status['code']



        # Record policy bought by customer via 'Customer' microservice
        cust_policy = policy_creation['data']
        cust_policy['cust_nric'] = receipt['customer_id']
        if cust_policy['category'] == 'Critical Illness':
            cust_policy['monthly_premium'] = policyPrice

        customer_policy_status = invoke_http(customer_policy_url, method='POST', json = cust_policy)
        print("Customer_policy record status:", customer_policy_status)

        # Check for valid response - if invalid, return error. 
        code = customer_policy_status["code"]

        if code not in range(200, 300):  
            print('\n-----Error with Customer microservice-----')  
            return jsonify(customer_policy_status), customer_policy_status['code']



        # Convert 'receipt' dict into json to send via AMQP
        message = json.dumps(receipt)

        # Send AMPQ message to 'Notification' microservice
        print('\n\n-----Publishing the message with routing_key=payment.success-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="payment.success", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))



        print('\n-----Purchase/Payment process completed-----')  
        receipt['code'] = 200
        
        response = jsonify(receipt)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    else:
        print(payment.error)
        return jsonify({code: 500, "success":success, "message": "Payment not executed by paypal", "error_paypal": payment.error}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)