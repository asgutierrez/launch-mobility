from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User, UserValidator
from database import db


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def configure_routes(app):

    @app.route('/api/auth/register', methods=['POST'])
    def register():
        try:
            user_data = UserValidator.parse_obj(request.json)
        except ValidationError as e:
            return Response(str(e), status=400)

        existing_user = User.query.filter_by(email=user_data.email).first()
        if existing_user:
            return Response("Email already exists", status=400)

        user_data.password = generate_password_hash(user_data.password)
        new_user = User(user_data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(f'User {new_user.email} registered')

    @app.route('/api/auth/token', methods=['POST'])
    def token():
        try:
            user_data = UserValidator.parse_obj(request.json)
        except ValidationError as e:
            return Response(str(e), status=400)

        existing_user = User.query.filter_by(email=user_data.email).first()
        if not existing_user:
            return Response("Email is not registered", status=400)

        if not check_password_hash(existing_user.password, user_data.password):
            return Response("Incorrect password", status=400)

        access_token = create_access_token(identity=existing_user.id)
        return jsonify({"token": access_token, "user_id": existing_user.id})
