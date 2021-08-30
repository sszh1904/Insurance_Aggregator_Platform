from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from invokes import invoke_http

import os, json

app = Flask(__name__)
CORS(app, support_credentials=True)

cust_db_check_url = os.environ.get('cust_db_check_url') or "http://localhost:5002/customer_details"
agent_getall_url = os.environ.get('agent_getall_url') or "http://localhost:5200/agents"
agent_cust_url = os.environ.get('agent_cust_url') or "http://localhost:5200/add_agent_customer"
add_cust_url = os.environ.get('add_cust_url') or "http://localhost:5002/customer"


@app.route("/register", methods=['POST'])
def register():

    if request.is_json:
        # Pull data from form via POST
        cust_nric = request.json.get("cust_nric")
        cust_password = request.json.get("cust_password")
        cust_email = request.json.get('cust_email')

        # Check if user/nric already exists in DB
        db_check_response = invoke_http(cust_db_check_url + "/" + cust_nric)

        code = db_check_response["code"]

        if code == 200:  # means user already exist in DB
            print('\n-----User/Customer already registered in DB-----') 
            db_check_response['code'] = 403
            db_check_response['message'] = 'User already exists. Hence, cannot register again.' 
            return jsonify(db_check_response), db_check_response['code'] # Cannot proceed to register

        # Singpass
        singpass_response = invoke_http("https://sandbox.api.myinfo.gov.sg/com/v3/person-sample/"+ cust_nric)
        
        # Pull list of agents and randomly choose 1 to allocate to customer
        agent_id = get_allocated_agent()

        # Create dict to pass as JSON
        agent_cust_details = {
            'nric':cust_nric,
            'agent_id':agent_id
        }

        # Record this customer-agent pairing in 'Agent' microservice
        register_agent = invoke_http(agent_cust_url, method='POST', json=agent_cust_details)
        
        # Check for valid response - if invalid, return error. 
        code = register_agent["code"]

        if code not in range(200, 300):  
            print('\n-----Error with Agent microservice-----')  
            return jsonify(register_agent), register_agent['code']

        address_obj = singpass_response['regadd']

        cust_details = {
            'name': singpass_response['name']['value'],
            'nric': cust_nric, 
            'sex': singpass_response['sex']['code'],
            'dob': singpass_response['dob']['value'],
            'email': cust_email, 
            'password': cust_password, 
            'mobile_no': singpass_response['mobileno']['nbr']['value'],
            'address': address_obj['street']['value'] + " " + address_obj['floor']['value'] + "-" + address_obj['unit']['value'] + " S(" + address_obj['postal']['value'] + ")",
            'agent_id': agent_id
        }

        print(cust_details)
        
        # Create/Register customer
        register_result = invoke_http(add_cust_url, method='POST', json=cust_details)

        return jsonify(register_result), register_result['code']

    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500


def get_allocated_agent():
    # Get all agents
    agents_json= invoke_http(agent_getall_url)
    print(agents_json)
    agent_list = agents_json["data"]["agents"]
    print('\n------- List of agents: -------')
    print(agent_list)

    # Randomly pick 1 agent
    random_agent = random.choice(agent_list)
    print('\n------- Randomly picked agent: -------')
    print(random_agent)
    return random_agent['agent_id']


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for Account Registration...")
    app.run(host="0.0.0.0", port=5005, debug=True)
