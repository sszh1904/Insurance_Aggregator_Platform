from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import requests

from invokes import invoke_http

app = Flask(__name__)
CORS(app)

customer_url = os.environ.get('customer_policy_viewer_url') or "http://localhost:5002/agent_custs_details"
agent_url = os.environ.get('agent_customer_url')  or "http://localhost:5200/getAgentCustomer"


@app.route("/viewAgentCusts/<string:agent_id>")
def view_cust_policies(agent_id):
    
    print("\nReceived a request from agent_id: " + agent_id)

    # request for agent's list of customers
    print('\n-----Invoking Agent microservice-----')
    agent_cust_list = invoke_http(agent_url + "/" + agent_id)

    # Check for valid response - if invalid, return error. 
    code = agent_cust_list["code"]

    if code not in range(200, 300):  
        print('\n-----Agent does not have customers----')  
        return jsonify(agent_cust_list), agent_cust_list['code']

    print("\nAgent's customer list:")
    print(agent_cust_list)

    # Get NRICs list
    nric_list = agent_cust_list['data']

    print('\n\n-----Invoking customer microservice-----')

    # Create dict to pass as json
    nric_json = {
        "nric_list": nric_list
    }

    # Retrieve agent's list of customers details 
    retrieve_custs = invoke_http(customer_url, method='POST', json=nric_json)

    # Check for valid response - if invalid, return error. 
    code = retrieve_custs["code"]

    if code not in range(200, 300):  
        print('\n-----Error with Customer microservice-----')  
        return jsonify(retrieve_custs), retrieve_custs['code']

    return jsonify({
        "code": 200,
        "data": {
            "cust_list": retrieve_custs["data"],
        }
    }), 200


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5400, debug=True)