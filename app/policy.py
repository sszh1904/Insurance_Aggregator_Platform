from flask import Flask, request, jsonify
from flask_cors import CORS

from invokes import invoke_http 

import os, sys

app = Flask(__name__)
CORS(app)

aviva_URL = os.environ.get('aviva_url') or "http://localhost:2001/aviva/"
ge_URL = os.environ.get('great_eastern_url') or "http://localhost:2002/great_eastern/"
aia_URL = os.environ.get('aia_url') or "http://localhost:2003/aia/"

categories = ['whole_life', 'critical_illness', 'savings']
companies = ['Aviva', 'Great Eastern', 'AIA']


@app.route("/getPoliciesByCategory/<string:cat>")
def getPoliciesByCategory(cat):
    # Simple input validation
    if cat in categories:
        try:
            print("\nReceived a request - policy category:", cat)

            # do the actual work
            result = aggregate_policies(cat)
            return jsonify(result), result['code']

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "policy.py internal error: " + ex_str
            }), 500
            

    # if reached here, invalid category sent through request
    return jsonify({
        "code": 404,
        "message": "Category not found."
    }), 404

def aggregate_policies(cat):
    aggregated = []

    # Aviva
    print('\n-----Invoking Aviva API-----')
    aviva_response = invoke_http(aviva_URL + 'category/' + cat)
    print('aviva_response: ', aviva_response)

    # Check if there is a valid response - if no, return error. Else, add policies into aggregated list
    code = aviva_response["code"]

    if code not in range(200, 300):
        print('\n-----Error with Aviva API-----')  
        return aviva_response
    
    for policy in aviva_response['data']:
        policy['company'] = "Aviva"

    print('\n-----Aggregating Aviva policies-----')
    aggregated.extend(aviva_response['data'])
    print('\n... Done')

    # AIA
    print('\n-----Invoking AIA API-----')
    aia_response = invoke_http(aia_URL + 'category/' + cat)
    print('aia_response: ', aia_response)

    # Check if there is a valid response - if no, return error. Else, add policies into aggregated list
    code = aia_response["code"]

    if code not in range(200, 300):  
        print('\n-----Error with AIA API-----')  
        return aia_response
    
    for policy in aia_response['data']:
        policy['company'] = "AIA"

    print('\n-----Aggregating AIA policies-----')    
    aggregated.extend(aia_response['data'])
    print('\n... Done')


    # Great Eastern
    print('\n-----Invoking Great Eastern API-----')
    ge_response = invoke_http(ge_URL + 'category/' + cat)
    print('ge_response: ', ge_response)

    # Check if there is a valid response - if no, return error. Else, add policies into aggregated list
    code = ge_response["code"]

    if code not in range(200, 300):  
        print('\n-----Error with Great Eastern API-----')  
        return ge_response
    
    for policy in ge_response['data']:
        policy['company'] = "Great Eastern"

    print('\n-----Aggregating Great Eastern policies-----')    
    aggregated.extend(ge_response['data'])
    print('\n... Done')

    print('\n-----Returning aggregated policies-----')
    print('\n... Done')

    return {
            "code": 200,
            "data": aggregated
        }


@app.route("/getPolicyById/<string:policy_id>/<string:company>")
def getPolicyById(policy_id, company):
    # Simple input validation
    if company in companies:
        try:
            print(f"\nReceived a request a policy's details: {policy_id}, {company}")

            # do the actual work
            result = retrieve_policy(policy_id, company)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "policy.py internal error: " + ex_str
            }), 500

    # if reached here, invalid category/company sent through request
    return jsonify({
        "code": 404,
        "message": "Company not found."
    }), 404

def retrieve_policy(policy_id, company):
    url = f'id/{policy_id}'

    # making the correct url/endpoint to call
    if company == 'Aviva':
        url = aviva_URL + url
    elif company == 'Great Eastern':
        url = ge_URL + url
    else:
        url = aia_URL + url

    print(f'\n-----Invoking {company} API-----')
    response = invoke_http(url)
    print('response: ', response)

    return response


@app.route("/createpolicy/<string:policy_id>")
def createPolicy(policy_id):
    try:
        print(f"\nCreating insurance policy based on policy_id: {policy_id}")

        # do the actual work
        result = create_policy(policy_id)
        return jsonify(result), result["code"]

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "policy.py internal error: " + ex_str
        }), 500

def create_policy(policy_id):
    url = f'/createpolicy/{policy_id}'

    # making the correct url/endpoint to call
    if policy_id[:2] == 'AV':
        url = aviva_URL + url
    elif policy_id[:2] == 'GE':
        url = ge_URL + url
    else:
        url = aia_URL + url

    response = invoke_http(url)
    print('response: ', response)

    return response

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for retrieving and aggregating policies...")
    app.run(host="0.0.0.0", port=5000, debug=True)