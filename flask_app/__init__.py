import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db_path = 'mysql://user:password@127.0.0.1:3306/db'
env = os.getenv('EXE_ENV')
if env == 'testing':
    db_path = 'sqlite:////tmp/test.db'
if env == 'container':
    db_path = 'mysql://user:password@mysql:3306/db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()
