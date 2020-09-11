from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key = "11111111"

app.config.from_object('configs.default-setting')

db = SQLAlchemy(app)
