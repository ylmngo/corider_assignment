from flask import request, Response, url_for
from mongoengine import ValidationError, DoesNotExist 
from core import cache
from core.apis import decorators
from .service import UserService
from . import user_resource
from bson import json_util
import json

@user_resource.route('/', methods=["POST"], strict_slashes=False)
@decorators.accept_payload
def create_user(payload): 
    try:
        resp = UserService.create_user(payload=payload)
        return Response(resp.to_json(), status=200, mimetype="application/json")
    except Exception as e: 
        if e is ValidationError: 
            return Response("Invalid user data: " + str(e), status=400) 
        return Response("Server Error: " + str(e), status=500)
    
    
@user_resource.route('/', methods=["GET"], strict_slashes=True) 
@cache.cached(timeout=50, query_string=True)
def list_users(): 
    per_page = 5
    page = int(request.args.get("page", 1))

    try:
        users = UserService.list_users(page, per_page=per_page)
        user_count = UserService.get_collection_len()
        
        links = {
            "self": {"href": url_for(".list_users", page=page, _external=True)},
            "last": {
                "href": url_for(
                    ".list_users", page=(user_count // per_page) + 1, _external=True
                )
            },
        }
        if page > 1:
            links["prev"] = {
                "href": url_for(".list_users", page=page - 1, _external=True)
            }
        if page - 1 < (user_count // per_page):
            links["next"] = {
                "href": url_for(".list_users", page=page + 1, _external=True)
            }

        resp = json_util.dumps({
            "users": users, 
            "_links": links
        })
            
        return Response(response=resp, status=200, mimetype="application/json")
        
    except Exception as e: 
        return Response(response="Server error: " + str(e), status=400)
    
@user_resource.route('/<id>', methods=["GET"], strict_slashes=True)
@cache.memoize(timeout=50)
def get_user(id): 
    try: 
        resp = UserService.get_user_by_id(id=id)
        return Response(response=resp.to_json(), status=200, mimetype="application/json")
    except Exception as e: 
        return Response("Invalid user id", status=404)
    
@user_resource.route('/<id>', methods=["PUT"], strict_slashes=False) 
@decorators.accept_payload
def update_user(payload, id): 
    try:
        user = UserService.get_user_by_id(id=id)
        query = UserService.validate_query(payload=payload) 
        user.update(**query)
        return Response(response=user.to_json(), status=200, mimetype="application/json")
    except Exception as e:  
        if e is DoesNotExist:
            return Response("Invalid user id", status=404)
        return Response("Unable to update user: " + str(e), status=400)
        

@user_resource.route('/<id>', methods=["DELETE"], strict_slashes=False) 
def delete_user(id): 
    try: 
        user = UserService.get_user_by_id(id=id)
        user.delete()
        return Response("User succesfully deleted", status=200)
    except Exception as e: 
        if e is DoesNotExist: 
            return Response("Invalid user id", status=404)
        return Response("Unable to delete user: " + str(e), status=400)
