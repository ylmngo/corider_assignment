from flask import request, Response, jsonify
from core import db
from . import UserIn, UserOut, UserUpdate
from bson import ObjectId, json_util
import json 
from . import user_resource, decorators

@user_resource.route('/', methods=["POST"], strict_slashes=False)
@decorators.accept_payload
def create_user(payload): 
    try: 
        user = UserIn(**payload)
        doc = db.Users.insert_one(user.to_bson())
        user.id = ObjectId(str(doc.inserted_id))
        resp = user.to_json()
        return resp
    except Exception as e: 
        return Response("Invalid user data: " + str(e), status=400)
    
@user_resource.route('/', methods=["GET"], strict_slashes=True) 
def list_users(): 
    docs = db.Users.find(projection={"password": 0})
    resp = [UserOut(**doc).to_json() for doc in docs]
    return resp

    
@user_resource.route('/<id>', methods=["GET"], strict_slashes=True)
def get_user(id): 
    try: 
        doc = db.Users.find_one({"_id": ObjectId(id)}, projection={"password": 0})
        if not doc: 
            raise Exception()
        resp = UserOut(**doc).to_json() 
        return resp 
    except Exception as e: 
        return Response("Invalid user id: " + str(e), status=404)
    
@user_resource.route('/<id>', methods=["PUT"], strict_slashes=False) 
@decorators.accept_payload
def update_user(payload, id): 
    updateQuery = {} 
    if "email" in payload: 
        updateQuery["email"] = payload["email"]
    if "name" in payload: 
        updateQuery["name"] = payload["name"]
    if "password" in payload: 
        updateQuery["password"] = payload["password"]
    
    try: 
        doc = db.Users.find_one_and_update({"_id": ObjectId(id)}, {"$set": updateQuery})
        resp = UserOut(**doc)
        if "email" in updateQuery: 
            resp.email = updateQuery["email"]
        if "name" in updateQuery:         
            resp.name  = updateQuery["name"] 
        resp = resp.to_json()
        return resp 
    except Exception as e: 
        return Response("Unable to update user: " + str(e), status=400)

@user_resource.route('/<id>', methods=["DELETE"], strict_slashes=False) 
def delete_user(id): 
    try: 
        doc = db.Users.find_one_and_delete({"_id": ObjectId(id)})
        return Response("User Deleted", status=200)
    except Exception as e: 
        return Response("Unable to delete user: " + str(e), status=400)
