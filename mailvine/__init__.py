from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt     #hash passwords
from flask_login import LoginManager    #manage loggins, makes sessions

# from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret Key to protect data. Protection against cookie data tampering.
app.config['SECRET_KEY'] = '2a44893ff4337692349481e9a9e77e75'
# URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailvine.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mailvine import routes

# TODO: fix positioning of flash messages
# TODO: fix positioning of account and log out buttons in dashboard
