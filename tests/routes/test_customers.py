from unittest.mock import patch

from flask import Flask
import json
import sys, os

from flask_jwt_extended import JWTManager, create_access_token
from flask_migrate import Migrate

sys.path.append(os.path.abspath(''))

from routes.customers import configure_routes as customers_routes
from database import FULL_URL_DB, db


def configure_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config['CELERY_BROKER_URL'] = os.environ.get('REDISGREEN_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    jwt = JWTManager(app)
    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    return app


def get_test_token():
    return create_access_token(identity="1")


@patch('routes.customers.save_customer')
@patch('models.customer.Customer')
def test_post_route__success(save_customer_mock, customer_mock):

    app = configure_app()
    customers_routes(app)
    client = app.test_client()
    url = '/api/customers'
    with app.app_context():
        token = get_test_token()

    mock_request_headers = {
        'Authorization': f'Bearer {token}'
    }

    mock_request_data = {
        "email": "prueba8@",
        "first_name": "prueba",
        "last_name": "prueba",
        "zip_code": "08989"
    }

    mock_response_data = {
        "email": "prueba8@",
        "first_name": "prueba",
        "last_name": "prueba",
        "zip_code": "08989",
        'id': None,
        'middle_name': None,
        'state': 'NJ',
        'user_id': '1',
        'city': 'New Brunswick',
        'county': 'Middlesex'
    }

    customer_filter_by_mock = customer_mock.query.filter_by
    customer_filter_by_mock.return_value = None

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers, content_type='application/json')

    assert response.status_code == 200
    assert response.json == mock_response_data