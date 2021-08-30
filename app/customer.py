from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('customerDB') or 'mysql+mysqlconnector://root@localhost:3306/customer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)  

class Customer(db.Model):
    __tablename__ = 'customer'
    cust_name = db.Column(db.String(64), nullable=False)
    cust_nric = db.Column(db.String(9), nullable=False, primary_key=True)
    cust_sex= db.Column(db.String(1), nullable=False)
    cust_dob = db.Column(db.String(20), nullable = False)
    cust_email=db.Column(db.String(100), nullable=False)
    cust_password = db.Column(db.String(20), nullable = False)
    mobile_no = db.Column(db.String(15))
    address = db.Column(db.String(100))
    agent_id = db.Column(db.String(100), nullable = False)

    def __init__(self, cust_name, cust_nric, cust_sex, cust_dob, cust_email, cust_password, mobile_no, address, agent_id):
        self.cust_name = cust_name
        self.cust_nric = cust_nric
        self.cust_sex = cust_sex
        self.cust_dob = cust_dob
        self.cust_email = cust_email
        self.cust_password = cust_password
        self.mobile_no = mobile_no
        self.address = address
        self.agent_id = agent_id

    def json(self):
        return {"cust_name":self.cust_name, "cust_nric":self.cust_nric, "cust_sex":self.cust_sex, "cust_dob":self.cust_dob, "cust_email":self.cust_email, "cust_password":self.cust_password, "mobile_no":self.mobile_no, "address":self.address, "agent_id":self.agent_id}


class Cust_Policies(db.Model):
    __tablename__ = 'cust_policies'
    cust_nric = db.Column(db.String(9),nullable = False, primary_key = True)
    policy_id = db.Column(db.String(100), nullable = False)
    policy_creation_id = db.Column(db.String(100), nullable = False, primary_key = True)
    policy_name = db.Column(db.String(100),nullable = False)
    policy_category = db.Column(db.String(100),nullable = False)
    monthly_premium = db.Column(db.String(100),nullable = False)
    coverage = db.Column(db.String(100))
    sum_insured = db.Column(db.String(100))
    num_condition_covered = db.Column(db.String(100))
    rate_of_return_per_annum = db.Column(db.String(100))
    initial_deposit = db.Column(db.String(100))

    def __init__(self, cust_nric, policy_id, policy_creation_id, policy_name, policy_category, monthly_premium, coverage, num_condition_covered, sum_insured,  rate_of_return_per_annum, initial_deposit):
        self.cust_nric = cust_nric
        self.policy_id = policy_id
        self.policy_creation_id = policy_creation_id
        self.policy_name = policy_name
        self.policy_category=policy_category
        self.monthly_premium=monthly_premium
        self.coverage=coverage
        self.sum_insured=sum_insured
        self.num_condition_covered=num_condition_covered
        self.rate_of_return_per_annum=rate_of_return_per_annum
        self.initial_deposit=initial_deposit

    def json(self):
        return {
            "cust_nric": self.cust_nric,
            "policy_id":self.policy_id,
            "policy_creation_id":self.policy_creation_id,
            "policy_name":self.policy_name,
            "policy_category":self.policy_category,
            "monthly_premium":self.monthly_premium,
            "coverage":self.coverage,
            "sum_insured":self.sum_insured,
            "num_condition_covered":self.num_condition_covered,
            "rate_of_return_per_annum" : self.rate_of_return_per_annum,
            "initial_deposit" : self.initial_deposit
        }


# Retrieve a list of all customers
@app.route("/customer")
def get_all():
    custlist = Customer.query.all()
    if len(custlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "customers": [cust.json() for cust in custlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no customers."
        }
    ), 404


# Retrieve list of policies bought by a customer
@app.route("/viewPolicies/<string:nric>")
def view_cust_policies(nric):
    result = Cust_Policies.query.filter_by(cust_nric=nric).first()
    
    if result:
        cust_pol = Cust_Policies.query.filter_by(cust_nric=nric)

        return jsonify(
            {
                "code": 200,
                "data": [cust.json() for cust in cust_pol]
            }

        )
    return jsonify(
        {
            "code": 404,
            "message": "Customer has no policies"
        }
    ), 404


# Customer Login Authentication
@app.route("/customerlogin", methods=['POST'])
def login_by_cust_nric():
    if request.is_json:
        cust_details = request.get_json()
        cust_nric = cust_details['cust_nric']
        cust_password = cust_details['cust_password']
        print(cust_nric)
        print(cust_password)
        customer = Customer.query.filter_by(cust_nric=cust_nric).first()
        if customer:
            if customer.cust_password == cust_password:
                return jsonify(
                    {
                        "code": 200,
                        "data": customer.json()
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 403,
                        "message": "Wrong password."
                    }
                ), 403

        return jsonify(
            {
                "code": 404,
                "message": "Customer not found."
            }
        ), 404
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500


# Retrieve details of a customer
@app.route("/customer_details/<string:cust_nric>")
def get_by_cust_nric(cust_nric):
    
    customer = Customer.query.filter_by(cust_nric=cust_nric).first()

    if customer:
        print("Customer exist")

        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
        
    print("Customer doesn't exist")
    return jsonify(
        {
            "code": 404,
            "message": "No user found."
        }
    ), 404


# Add new customer
@app.route("/customer", methods=['POST'])
def addCustomer():
    if request.is_json:
        cust_details = request.get_json()

        customer = Customer(
            cust_name = cust_details['name'],
            cust_nric = cust_details['nric'],
            cust_sex = cust_details['sex'],
            cust_dob = cust_details['dob'],
            cust_email = cust_details['email'],
            cust_password = cust_details['password'],
            mobile_no = cust_details['mobile_no'],
            address = cust_details['address'],
            agent_id = cust_details['agent_id']
            )
        
        print('Object created')

        try:
            db.session.add(customer)
            db.session.commit()

        except Exception as e:
            print("\n Error in committing to database")
            print(e)
            print(e.body)

            return jsonify(
                {
                    "code":500,
                    "data": {
                        "cust_nric": cust_details['nric']
                    },
                    "message": "An error occurred when creating the new customer"
                }
            ), 500

        return jsonify(
            {
                "code":201,
                "data":customer.json()
            }
        ), 201
        
    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

# Add the newly bought policy for the customer
@app.route("/add_cust_policy", methods=['POST'])
def add_policy():
    print("\n Inside Customer Microservice")

    data = request.get_json()

    coverage = None
    sum_insured = None
    num_condition_covered = None
    rate_of_return_per_annum = None
    initial_deposit = None

    if data['category'] == 'Whole Life':
        coverage = ", ".join(data['coverage'])
        sum_insured = data['sum_insured']
        
    elif data['category'] == 'Critical Illness':
        num_condition_covered = data['num_condition_covered']
        sum_insured = data['sum_insured']
        
    else:
        rate_of_return_per_annum = data['rate_of_return_per_annum']
        initial_deposit = data['initial_deposit']


    policy = Cust_Policies(
        cust_nric = data['cust_nric'],
        policy_id = data['policyId'],
        policy_creation_id = data['policy_creation_id'],
        policy_name = data['name'],
        policy_category = data['category'],
        monthly_premium = data['monthly_premium'],
        coverage = coverage,
        sum_insured = sum_insured,
        num_condition_covered = num_condition_covered,
        rate_of_return_per_annum = rate_of_return_per_annum,
        initial_deposit = initial_deposit
    )

    print("\n Object created")

    try:
        db.session.add(policy)
        db.session.commit()
        
    except Exception as e:
        print("\n Error in committing to database")
        print(e)
        print(e.body)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred when adding the policy for customer."
            }
        ), 500

    print("\n Committed to database")
    return jsonify(
        {
            "code": 201,
            "data": policy.json()
        }
    ), 201


# Retrieve an agent's list of customers details 
@app.route("/agent_custs_details", methods=['POST'])
def get_agent_custs_details():
    if request.is_json:
        data = request.get_json()
        nrics = data['nric_list']

        customers = Customer.query.filter(Customer.cust_nric.in_(nrics))

        return jsonify({
            "code": 200,
            "data": [cust.json() for cust in customers]
        }), 200

    else:
        return jsonify(
            {
                "code": 500,
                "message": 'Input is not JSON.'
            }
        ), 500

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)