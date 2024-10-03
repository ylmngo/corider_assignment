from core import app
from flask import jsonify


@app.route('/')
def ready(): 
    resp = jsonify({
        "status": "ready", 
        "env": "dev"
    }) 

    return resp 
