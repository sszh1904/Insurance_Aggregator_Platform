from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from invokes import invoke_http

import os, sys
import operator
from operator import itemgetter
import collections
from collections import Counter

app = Flask(__name__)
CORS(app, support_credentials=True)

customer_url = os.environ.get('customer_url') or "http://localhost:5002/customer_details"
policy_URL = os.environ.get('policy_url') or "http://localhost:5000/getPoliciesByCategory"


@app.route("/getRecPolicies", methods=['POST'])
def get_rec_policies():
    print(request)
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            user = request.get_json()
            # user consist of user_inputs and userid
            print("\nReceived details of user in JSON:", user)

            # Process all the policies and return recco ones 
            rec_policies = policyProcessing(user)
            print('\n------------------------')
            print('\nresult: ', rec_policies)
            return jsonify(rec_policies), rec_policies["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "recommendation.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def policyProcessing(user):
    """
        Retrieve policies relevant to category
        invoke the policy microservice
    """
    category = user['category']

    print("\n----- invoking policy microservice ----- ")
    policies = invoke_http(policy_URL+"/"+category, method='GET')
    print('policies relevant to category returned:', policies)

    """
        Retrieve customer details with respect to userid
        invoke the customer microservice
    """
    
    nric = user['nric']

    print("\n----- invoking customer microservice ----- ")
    customer_details = invoke_http(customer_url + '/' + nric)
    print("customer details returned:", customer_details)

    # rank based difference monthly premium
    user_dob = customer_details['data']["cust_dob"]

    year = user_dob[:4]
    print(year)
    age = 2021 - int(year)

    policies_eligible = policies['data']
    eligible_policy = []
    
    # for Savings
    if category=="savings":
        selected_policies = {0: [], 1: [], 2: [], 3: []}
        for policy in policies_eligible:
            fulfilled = 0
            
            diff_budget_premium = user['monthly_budget'] - policy['monthly_premium']
            if diff_budget_premium >= 0:
                fulfilled += 1
            diff_initial_deposit = user['initial_deposit'] - policy['initial_deposit']
            if diff_initial_deposit >= 0:
                fulfilled += 1
            diff_returns = int(user['returns'][0]) - policy['rate_of_return_per_annum']
            if diff_returns <= 0:
                fulfilled += 1
            
            selected_policies[fulfilled].append(policy)
           
        print('selected_policies: ', selected_policies)
         
        recommended_pol = []
        a = 3
        while len(recommended_pol) < 5:
            policy_budget_score = {}
            policy_initial_dep_score = {}
            policy_rates_expected_score = {}
            policy_scores = {}
            for policy in selected_policies[a]:    
                policy_budget_score[policy['policyId']] = policy['monthly_premium']
                policy_initial_dep_score[policy['policyId']] = policy['initial_deposit']
                policy_rates_expected_score[policy['policyId']] = policy['rate_of_return_per_annum']
                policy_scores[policy['policyId']] = 0
            print('populating policy dictionaries')    
            # ranking them based on diff_premium_budget
            sort_budget_score = dict(sorted(policy_budget_score.items(), key = operator.itemgetter(1))) 
            # rank them based on intial deposit
            sort_initial_dep_score = dict(sorted(policy_initial_dep_score.items(), key = operator.itemgetter(1))) 

            # rank them based on rates returned
            sort_rates_score = dict(sorted(policy_rates_expected_score.items(), key = operator.itemgetter(1), reverse=True)) 
            
            factors = [sort_budget_score, sort_initial_dep_score, sort_rates_score]
            print(factors)
            for factor in factors:
                rank = len(factor)
                for sorted_policy in factor:
                    print(sorted_policy)
                    policy_scores[sorted_policy] += rank
                    rank -= 1
            
            sorted_policy_scores = dict(sorted(policy_scores.items(), key = operator.itemgetter(1))) 
            for top_policy in sorted_policy_scores:
                if len(recommended_pol) == 5:
                    break
                for policy in policies_eligible:
                    if policy['policyId'] == top_policy:
                        recommended_pol.append(policy)
            print('round',str(a) + ':', recommended_pol)
            a -= 1
        
        return {
            "code": 200,
            "data": {
                "recommended_policies": recommended_pol,
            }
        }
                
    elif category =="whole_life":
        policy_diff_budget_score = {}
        policy_sum_insured_score = {}
        policy_coverage_score = {}

        for policy in policies_eligible:
            if(user['monthly_budget'] >= policy['monthly_premium']):
                eligible_policy.append(policy)
                policies_eligible.remove(policy)
        while(len(eligible_policy) < 5 ):
            for policy in policies_eligible:
                eligible_policy.append(policy)
                if(len(eligible_policy) == 5 ):
                    break
        for policy in eligible_policy:
            # rank based difference monthly premium
            diff_budget_premium = user['monthly_budget'] - policy['monthly_premium']
            policy_diff_budget_score[policy['policyId']] = diff_budget_premium

            # rank based on sum insured 
            sum_insured = policy['sum_insured']
            policy_sum_insured_score[policy['policyId']] = sum_insured

            # rank based on coverage 
            num_coverage = len(policy['coverage'])
            policy_coverage_score[policy['policyId']] = num_coverage


        # ranking them based on diff_premium_budget
        sort_diff_budget_score = dict(sorted(policy_diff_budget_score.items(), key = operator.itemgetter(1))) 
        # rank them based on intial deposit
        sort_sum_insured_score = dict(sorted(policy_sum_insured_score.items(), key = operator.itemgetter(1))) 

        # rank them based on rates returned
        sort_coverage_score = dict(sorted(policy_coverage_score.items(), key = operator.itemgetter(1))) 

        print("\n----- sorted dictionaries ----- ")
        print("\ndiff_budget_score returned:", sort_diff_budget_score)  
        print("\ninitial sum_insured returned:", sort_sum_insured_score)  
        print("\n coverage score returned:", sort_coverage_score) 
        # get combined scoring 

        rank_desc = len(policies_eligible)
        for each in sort_diff_budget_score:
            sort_diff_budget_score[each] = rank_desc
            rank_desc-= 1
        
        rank_desc = len(policies_eligible)
        for each in sort_sum_insured_score:
            sort_sum_insured_score[each] = rank_desc
            rank_desc-= 1
        
        rank_desc = len(policies_eligible)
        for each in sort_coverage_score:
            sort_coverage_score[each] = rank_desc
            rank_desc-= 1

         # get combined scoring 
        combined_scoring = {}
        for each in sort_diff_budget_score:
            total = 0 
            total += sort_diff_budget_score[each]
            total += sort_sum_insured_score[each]
            total += sort_coverage_score[each]
            combined_scoring[each] = total
        
        print("\n----- combined score ----- ")
        print("\ncombined scoring :", combined_scoring)  

        # total_count = Counter(combined_scoring)
        # # returning top 5 policies 
        # # {policyid: score}
        # top_policies = total_count.most_common(5)
        top_policies = []
        for each in list(reversed(list(combined_scoring)))[0:5]:
            top_policies.append(each)

        print("\n----- top policies ----- ")
        print("top policies returned:", top_policies)

        recommended_pol= []
        for policy in top_policies:
            for each in eligible_policy:
                if each['policyId'] == policy:
                    recommended_pol.append(each)

        print("\n----- recommended policies ----- ")
        print(recommended_pol)
        return {
            "code": 200,
            "data": {
                "recommended_policies": recommended_pol,
            }
        }

    elif category == "critical_illness": 
        if age >= 60:
            return {
                "code": 200,
                "data": {
                    "recommended_policies": [],
                    "message": "old"
                }
            }

        else:
            # print("\nhello", age)       
            policy_diff_budget_score = {}
            policy_num_conditions_score = {}
            policy_sum_insured_score = {}

            for policy in policies_eligible:
                # check premium based on age 
                if 16<= age <= 25 :
                    age_group = "16-25"
                elif 26 <= age <= 30:
                    age_group = "26-30"
                elif 31<= age <= 35:
                    age_group = "31-35"
                elif 36<= age <= 40:
                    age_group= "36-40"
                elif 41 <= age <=45:
                    age_group = "41-45"
                elif 46 <= age <= 50:
                    age_group = "46-50"
                elif 51 <= age <= 55:
                    age_group= "51-55"
                elif 56 <= age <= 59:
                    age_group = "56-59"
                
                cust_premium = policy['age_group_premium'][age_group]

               
                if(user['monthly_budget'] >= cust_premium):
                    eligible_policy.append(policy)
                    policies_eligible.remove(policy)
            
            while(len(eligible_policy) < 5 ):
                for policy in policies_eligible:
                    eligible_policy.append(policy)
                if(len(eligible_policy) < 5 ):
                    break
            for policy in eligible_policy:
                cust_premium = policy['age_group_premium'][age_group]
                diff_budget_premium = user['monthly_budget'] - cust_premium
                policy_diff_budget_score[policy['policyId']] = diff_budget_premium

                # rank based on num conditions  
                num_condition_covered = policy['num_condition_covered']

                policy_num_conditions_score[policy['policyId']] = num_condition_covered

                # rank based on sum_insured 
                sum_insured = policy['sum_insured']

                policy_sum_insured_score[policy['policyId']] = sum_insured

                

            # ranking them based on diff_premium_budget
            sort_diff_budget_score = dict(sorted(policy_diff_budget_score.items(), key = operator.itemgetter(1))) 
            # rank them based on intial deposit
            sort_num_conditions_score = dict(sorted(policy_num_conditions_score.items(), key = operator.itemgetter(1))) 

            # rank them based on rates returned
            sort_sum_insured_score = dict(sorted(policy_sum_insured_score.items(), key = operator.itemgetter(1))) 

            rank_desc = len(policies_eligible)
            for each in sort_diff_budget_score:
                sort_diff_budget_score[each] = rank_desc
                rank_desc-= 1

            rank_desc = len(policies_eligible)
            for each in sort_num_conditions_score:
                sort_num_conditions_score[each] = rank_desc
                rank_desc-= 1
            
            rank_desc = len(policies_eligible)
            for each in sort_sum_insured_score:
                sort_sum_insured_score[each] = rank_desc
                rank_desc-= 1
            
            # get combined scoring 
            combined_scoring = {}
            for each in sort_diff_budget_score:
                total = 0 
                total += sort_diff_budget_score[each]
                total += sort_num_conditions_score[each]
                total += sort_sum_insured_score[each]
                combined_scoring[each] = total
            
            print("\n----- combined score ----- ")
            print("\ncombined scoring :", combined_scoring)  

            # top_policies = total_count.most_common(5)
            top_policies = []
            for each in list(reversed(list(combined_scoring)))[0:5]:
                top_policies.append(each)
            print("\n----- top policies ----- ")
            print("top policies returned:", top_policies)

            # get the premium of the individual's age group 
            recommended_pol= []
            for policy in top_policies:
                for each in eligible_policy:
                    if each['policyId'] == policy:
                        # each['premium_derived'] = each['']
                        if 16<= age <= 25 :
                            age_group = "16-25"
                        elif 26 <= age <= 30:
                            age_group = "26-30"
                        elif 31<= age <= 35:
                            age_group = "31-35"
                        elif 36<= age <= 40:
                            age_group= "36-40"
                        elif 41 <= age <=45:
                            age_group = "41-45"
                        elif 46 <= age <= 50:
                            age_group = "46-50"
                        elif 51 <= age <= 55:
                            age_group= "51-55"
                        elif 56 <= age <= 59:
                            age_group = "56-59"
                        each['premium_derived'] = each['age_group_premium'][age_group]
                        recommended_pol.append(each)

            print("\n----- recommended policies ----- ")
            print(recommended_pol)
            return {
                "code": 200,
                "data": {
                    "recommended_policies": recommended_pol
                }
            }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for generating top-five recommended policies...")
    app.run(host="0.0.0.0", port=5001, debug=True)