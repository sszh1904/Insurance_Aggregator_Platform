from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ
import os, sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('transactionDB') or 'mysql+mysqlconnector://root:root@localhost:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Transaction(db.Model):
    __tablename__ = 'transaction'

    trans_id = db.Column(db.String(50), nullable=False, primary_key=True)
    cust_nric = db.Column(db.String(9), nullable=False)
    policy_creation_id = db.Column(db.String(20), nullable=False)
    trans_datetime = db.Column(db.String(30), nullable=False,)
    amount = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, trans_id, cust_nric, policy_creation_id, trans_datetime, amount):
        self.trans_id = trans_id
        self.cust_nric = cust_nric
        self.policy_creation_id = policy_creation_id
        self.trans_datetime = trans_datetime
        self.amount = amount

    def json(self):
        return {"trans_id": self.trans_id, "cust_nric": self.cust_nric, "policy_creation_id": self.policy_creation_id, "trans_datetime": self.trans_datetime, "amount": self.amount}



@app.route("/add_transaction", methods=['POST'])
def add_transaction():
    print("\n Inside Transaction Microservice")

    data = request.get_json()
    transaction = Transaction(data['trans_id'], data['cust_nric'], data['policy_creation_id'], data['trans_datetime'], data['amount'])
    print("\n Object created")

    try:
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        print("\n Error in committing to database")
        print(e)
        print(e.body)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the transaction."
            }
        ), 500

    print("\n Committed to database")
    return jsonify(
        {
            "code": 201,
            "data": transaction.json()
        }
    ), 201


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) + " for recording Transactions...")
    app.run(host='0.0.0.0', port=5008, debug=True)