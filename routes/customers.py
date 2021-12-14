from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from sqlalchemy import inspect

from models.customer import Customer, CustomerValidator
from database import db
from tasks.customer import update_customer_location_data

customers = Blueprint('customers', __name__)


@customers.route('/api/customers', methods=['POST'])
@jwt_required()
def create_customers():
    try:
        customer_data = CustomerValidator.parse_obj(request.json)
    except ValidationError as e:
        return Response(str(e), status=400)

    existing_customer = Customer.query.filter_by(email=customer_data.email).first()
    if existing_customer:
        return Response("Email already exists", status=400)

    current_user_id = get_jwt_identity()
    customer_data.user_id = current_user_id
    new_customer = Customer(customer_data)

    save_customer(new_customer)

    update_customer_location_data(db, new_customer, new_customer.zip_code)

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    return jsonify(object_as_dict(new_customer))


def save_customer(new_customer):
    db.session.add(new_customer)
    db.session.commit()



