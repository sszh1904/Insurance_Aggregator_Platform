from flask import Flask, request, jsonify
from flask_cors import CORS

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl

import amqp_setup

import json
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

app = Flask(__name__)

monitorBindingKey='payment.success'

def receivePaymentInfo():
    amqp_setup.check_setup()
    
    queue_name = "Payment_Success"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a successful payment by " + __file__)
    sendEmail(body)
    print() # print a new line feed

def sendEmail(message):
    print("Printing the email message:")
    try:
        info = json.loads(message)
        print("--JSON:", info)
        
        customer_name = info['customer_name']
        customer_email = info['email']
        price = info['price']
        policy_name = info['policy_creation']['name']
        policy_id = info['policy_id']
        payment_id = info['paymentID']
        create_time = info['create_time']
        policy_creation_id = info['policy_creation']['policy_creation_id']
        category = info['policy_creation']['category']
        policy_creation = info['policy_creation']

        policy_summary = f'Policy Creation ID: {policy_creation_id} <br> Policy Name: {policy_name} <br> Category: {category} <br> Monthly Premium: ${price} <br>'

        if category == 'Whole Life':
            coverage = ", ".join(policy_creation['coverage'])
            sum_insured = str(policy_creation['sum_insured'])
            policy_summary += f'Coverage: {coverage} <br> Sum Insured: ${sum_insured}'
        
        elif category == 'Critical Illness':
            conditions = str(policy_creation['num_condition_covered'])
            sum_insured = str(policy_creation['sum_insured'])
            policy_summary += f'Number Of Conditions Covered: {conditions} <br> Sum Insured: ${sum_insured}'
        
        else:
            rate = str(policy_creation['rate_of_return_per_annum'])
            initial_dep = str(policy_creation['initial_deposit'])
            policy_summary += f'Rate Of Return Per Annum: {rate}% <br> Initial Deposit: ${initial_dep}'
            
        email = Mail(
            from_email = 'esdg9t2@gmail.com',
            to_emails = customer_email,
            subject = f"Policy No: {policy_creation_id} - {policy_name}",
            html_content = f'Dear <strong>{customer_name}</strong>, <p>Your Insurance Policy has been successfully created!</p> <p><strong><u>Transaction Summary</u></strong> <br> Transaction ID: {payment_id} <br> Datetime: {create_time} <br> Payment (for 1st month): ${price} </p> <p><strong><u>Policy Summary</u></strong><br>' + policy_summary + '</p><p>Thank you for choosing Insurance Aggregator, HUAT AH!</p><p>ESDG9T2</p>')
        
        print(email)
        
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(email)
            print(response.status_code)
            
        except Exception as e:
            print(e)
            print(e.body)
        
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", message)
    print()

if __name__ == "__main__": 
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receivePaymentInfo()