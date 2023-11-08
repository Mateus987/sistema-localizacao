from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import redis

from src.rpc.rpc_client import GrpcClient

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

grpc = GrpcClient()

import src.models
import src.resources
import src.routes
