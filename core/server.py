from core import app, swagger_ui_blueprint, SWAGGER_URL
from flask import jsonify
from .apis.users.users import user_resource

app.register_blueprint(user_resource, url_prefix="/users")
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def ready(): 
    resp = jsonify({
        "status": "ready", 
        "env": "dev"
    }) 

    return resp 
