from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.infra.configs.connection import DBConnectionHandler

db_handler = DBConnectionHandler()

app = Flask(__name__)
from .routes import *