from flask_restful import reqparse, abort, Resource
from api.data.customers import Customer
from api.data import db_session
from flask import jsonify


class CustomerResource(Resource):
    def get(self, customer_id):
        abort_if_customer_not_found(customer_id)
        session = db_session.create_session()
        customer = session.query(Customer).get(customer_id)

        return jsonify({'customer': customer.to_dict(
            only=(
                'id', 'surname', 'name', 'email', 'hashed_password'
            ))})

    def delete(self, customer_id):
        abort_if_customer_not_found(customer_id)
        session = db_session.create_session()
        album = session.query(Customer).get(customer_id)
        session.delete(album)
        session.commit()
        return jsonify({'success': 'OK'})


class CustomerListResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('surname', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('hashed_password', required=True)
        args = parser.parse_args()
        session = db_session.create_session()
        album = Customer(
            surname=args["surname"],
            name=args["name"],
            email=args["email"],
            hashed_password=args["hashed_password"],
        )
        session.add(album)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        customers = session.query(Customer).all()
        return jsonify({'customer': [item.to_dict(
            only=(
                'id', 'surname', 'name', 'email', 'hashed_password'
            )) for item in customers]})


def abort_if_customer_not_found(jobs_id):
    session = db_session.create_session()
    customer = session.query(Customer).get(jobs_id)
    if not customer:
        abort(404, message=f"Customer {jobs_id} not found")
