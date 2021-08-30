from flask import Flask, request, jsonify
from flask_cors import CORS

from policy_data import aia_policies

import os, sys
from random import randint

app = Flask(__name__)
CORS(app)  

# retrieve all policies that belong to a category
@app.route("/aia/category/<string:cat>")
def get_by_category(cat):
    try:
        filter_cat = ''

        if cat == 'whole_life':
            filter_cat = 'Whole Life'
        elif cat == 'critical_illness':
            filter_cat = 'Critical Illness'
        elif cat == 'savings':
            filter_cat = 'Savings'

        if filter_cat:
            policies = []

            for policy in aia_policies:
                if policy['category'] == filter_cat:
                    policies.append(policy)
                
            return jsonify(
                {
                    "code": 200,
                    "data": policies
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Category not found."
                }
            ), 404

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "aia.py internal error: " + ex_str
        }), 500

# retrieve a policy, based on its policy_id
@app.route("/aia/id/<string:policy_id>")
def get_by_id(policy_id):
    try:
        output_policy = {}

        for policy in aia_policies:
            if policy['policyId'] == policy_id:
                output_policy = policy
                break
        
        if output_policy:
            return jsonify(
                {
                    "code": 200,
                    "data": output_policy
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Policy ID not found."
                }
            ), 404

    except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "aia.py internal error: " + ex_str
            }), 500

# create insurance policy
@app.route("/aia/createpolicy/<string:policy_id>")
def createpolicy(policy_id):
    try:
        output_policy = {}

        for policy in aia_policies:
            if policy['policyId'] == policy_id:
                output_policy = policy
                break
        
        if output_policy:
            policy_creation_id = "AIAPC"
            for i in range(6):
                policy_creation_id += str(randint(0, 9))
            
            output_policy['policy_creation_id'] = policy_creation_id

            return jsonify(
                {
                    "code": 200,
                    "data": output_policy
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Policy ID not found."
                }
            ), 404

    except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "aia.py internal error: " + ex_str
            }), 500

if __name__ == "__main__":  
    print("This is flask for " + os.path.basename(__file__) + ": retrieving AIA policies...")
    app.run(host='0.0.0.0', port=2003, debug=True)
