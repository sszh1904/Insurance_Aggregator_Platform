from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

import mysql.connector

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('agentDB') or 'mysql+mysqlconnector://root@localhost:3308/agent'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

#table for agent details
class Agent(db.Model):
    __tablename__ = 'agent'
    agent_name = db.Column(db.String(64),nullable=False)
    agent_id = db.Column(db.String(10), nullable = False, primary_key = True)
    agent_nric = db.Column(db.String(9), nullable = False)
    agent_password = db.Column(db.String(100), nullable = False)

    def __init__(self, agent_name, agent_nric, agent_id, agent_password):
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.agent_nric = agent_nric 
        self.agent_password = agent_password

    def json(self):
        return {"agent_name":self.agent_name,"agent_id":self.agent_id,"agent_nric": self.agent_nric, "agent_password":self.agent_password}



#table for agent and customer pairing
class AgentCustomer(db.Model):
    __tablename__ ='agentcustomer'
    agent_id = db.Column(db.String(10),nullable = False, primary_key = True)
    cust_nric = db.Column(db.String(9),nullable = False, primary_key = True)

    def __init__(self,agent_id,cust_nric):
        self.agent_id = agent_id
        self.cust_nric = cust_nric

    def json(self):
        return {"agent_id":self.agent_id, "cust_nric":self.cust_nric}



# Retrieve a list of all agents - to conduct for loop in Account complex microservice for allocation algo
@app.route("/agents")  
def get_all():
    agentlist = Agent.query.all()
    if len(agentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "agents": [agent.json() for agent in agentlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no agents"
        }
    ), 404

# Agent Login Authentication
@app.route("/agentlogin", methods=['POST'])
def login_by_cust_nric():
    if request.is_json:
        agent_details = request.get_json()
        agent_nric = agent_details['agent_nric']
        agent_password = agent_details['agent_password']
        print("Agent nric:",agent_nric)
        print("Agent password:", agent_password)
        agent = Agent.query.filter_by(agent_nric=agent_nric).first()
        if agent:
            if agent.agent_password == agent_password:
                return jsonify(
                    {
                        "code": 200,
                        "data": agent.json()
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
                "message": "Agent not found."
            }
        ), 404

# Retrieve details of an agent
@app.route("/agent_details", methods=['POST'])
def get_by_agent_id():
    if request.is_json:
        agent_details = request.get_json()
        agent_id = agent_details['agent_id']
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if agent:
            return jsonify(
                {
                    "code": 200,
                    "data": agent.json()
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "No agent found"
            }
        )

# Add record of randomly allocated agent and customer pair
@app.route("/add_agent_customer", methods=['POST'])
def add_agent_customer():
    if request.is_json:
        agent_cust_details = request.get_json()
        agent_customer = AgentCustomer(
            agent_id = agent_cust_details['agent_id'],
            cust_nric = agent_cust_details['nric']
        )
        print(getattr(agent_customer, 'cust_nric'))
        print(getattr(agent_customer,'agent_id'))

        try:
            db.session.add(agent_customer)
            db.session.commit()

        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "cust_nric": agent_cust_details['nric']
                    },
                "message": "An error occurred when creating the agent-customer pairing"
                }
            ), 500

        return jsonify(
            {
                "code": 201,
                "data": agent_customer.json(),
                "message": 'Agent Customer pair successfully created'
            }
        ), 201

    else:
        return jsonify(
            {
                "code": 500,
                "message": "Input is not in JSON"
            }
        )
    
# Retrieve a list of customer NRICs that are assigned to an agent
@app.route("/getAgentCustomer/<string:agent_id>")
def get_agent_customer(agent_id):
    check = AgentCustomer.query.filter_by(agent_id=agent_id).first()

    if check:
        customerList = AgentCustomer.query.filter_by(agent_id=agent_id)

        return jsonify(
            {
                "code": 200,
                "data": [cust.json()['cust_nric'] for cust in customerList]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Agent has no customers"
        }
    ), 404


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5200,debug=True)