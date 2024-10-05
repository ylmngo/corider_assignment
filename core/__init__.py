from flask import Flask 
from dotenv import load_dotenv
from pymongo import MongoClient
from mongoengine import connect 
from flask_swagger_ui import get_swaggerui_blueprint
import os 

load_dotenv() 
app = Flask(__name__) 

connect(db='users', host='127.0.0.1', port=27017)

client = MongoClient(os.environ.get("MONGO_URI"))
db = client.Users 


SWAGGER_URL = "/swagger" 
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL, 
    config={
        'app_name': "Corider Assignment"
    }
)
