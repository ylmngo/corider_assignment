from flask import request, Response
from mongoengine import ValidationError, DoesNotExist
from core import cache
from core.apis import decorators
from .service import UserService
from . import user_resource

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
    resp = UserService.list_users(page, per_page=per_page)
    return Response(response=resp.to_json(), status=200, mimetype="application/json")     
    
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
