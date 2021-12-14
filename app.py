import os

from flask import Flask
from flask_migrate import Migrate
from routes.customers import configure_routes as customer_routes
from routes.auth import configure_routes as auth_routes
from routes.tasks import configure_routes as tasks_routes
from database import db, FULL_URL_DB
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['CELERY_BROKER_URL'] = os.environ.get('REDISGREEN_URL', 'redis://localhost:6379/0')

jwt = JWTManager(app)
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

customer_routes(app)
auth_routes(app)
tasks_routes(app)
