from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret Key to protect data. Protection against cookie data tampering.
app.config['SECRET_KEY'] = '2a44893ff4337692349481e9a9e77e75'

# region DataBase structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailvine.db'
db = SQLAlchemy(app)
#endregion

from mailvine import routes