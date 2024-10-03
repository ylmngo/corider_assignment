from flask import Flask 
from dotenv import load_dotenv
from pymongo import MongoClient
import os 

load_dotenv() 
app = Flask(__name__) 
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.Users 

