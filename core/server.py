from core import app
from flask import jsonify
from .apis.users import user_resource

app.register_blueprint(user_resource, url_prefix="/users")

@app.route('/')
def ready(): 
    resp = jsonify({
        "status": "ready", 
        "env": "dev"
    }) 

    return resp 
