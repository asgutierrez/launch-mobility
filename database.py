from flask_sqlalchemy import SQLAlchemy

USER_DB = 'postgres'
PASS_DB = '1231853211a'
URL_DB = 'localhost'
NAME_DB = 'launch_mobility'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

db = SQLAlchemy()
