from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http

import os

app = Flask(__name__)
CORS(app)

policy_url = os.environ.get('checkout_policy_url') or "http://localhost:5000/getPolicyById"
customer_url = os.environ.get('checkout_customer_url') or "http://localhost:5002/customer_details"


@app.route("/checkout/<string:user_id>/<string:company>/<string:policy_id>/<string:monthly_premium>")
def displayPurchaseSummary(user_id, policy_id, company, monthly_premium):
    # make call to policy microservice and store result in variable
    policy_details = invoke_http(url=policy_url+'/{}/{}'.format(policy_id, company))

    # if policy retrieval fails, terminate
    code = policy_details["code"]
    if code not in range(200,300):
        #return error message 
        return jsonify({
            "code": code,
            "data": {"policy_details": policy_details},
            "message": "Failed to retrieve insurance policy details."
        }), code

    policy_name = policy_details['data']['name']

    if policy_details['data']['category'] == 'Critical Illness':
        policy_price = monthly_premium
    else:
        policy_price = policy_details['data']['monthly_premium']
    
    # make call to customer microservice and store result in variable
    customer_details = invoke_http(customer_url + '/' + user_id)
    # if customer details retrieval fails, terminate
    code = customer_details["code"]
    if code not in range(200,300):
        #return error message 
        return jsonify({
            "code" :code,
            "data": {"customer_details": customer_details},
            "message": "Failed to retrieve customer details."
        }), code
    customer_name = customer_details['data']['cust_name']
    email = customer_details['data']['cust_email']
    
    return jsonify({
        "code": 200,
        "data": {
            "user_id": user_id,
            "customer_name": customer_name,
            "email": email,
            "policy_id": policy_id,
            "policy_name": policy_name,
            "policy_price": policy_price
        }
    }), 200

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for retrieving Checkout details...")
    app.run(host="0.0.0.0", port=5003, debug=True)