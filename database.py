import os
from flask_sqlalchemy import SQLAlchemy

USER_DB = 'postgres'
PASS_DB = '1231853211a'
URL_DB = 'localhost'
NAME_DB = 'launch_mobility'
FULL_URL_DB = os.environ.get('DATABASE_URL', f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}')

if FULL_URL_DB and FULL_URL_DB.startswith("postgres://"):
    FULL_URL_DB = FULL_URL_DB.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()
