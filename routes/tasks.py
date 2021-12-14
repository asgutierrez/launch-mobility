from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.customer import Customer
from tasks.analytics import rank_zip_codes as rank_zip_codes_task
from tasks.gis import get_distance_between_zip_codes as get_distance_between_zip_codes_task


def configure_routes(app):
    @app.route('/api/tasks/rank', methods=['GET'])
    @jwt_required()
    def rank_zip_codes():
        return jsonify(rank_zip_codes_task(db))

    @app.route('/api/tasks/distance', methods=['GET'])
    @jwt_required()
    def get_distance_between_zip_codes():
        current_user_id = get_jwt_identity()
        existing_customer = Customer.query.filter_by(user_id=current_user_id).first()
        return jsonify(get_distance_between_zip_codes_task(existing_customer.zip_code))