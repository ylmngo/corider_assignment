from core.models.users import Users
from mongoengine import Document
from flask import jsonify

class UserService: 
    @staticmethod
    def create_user(payload): 
        user = Users(**payload) 
        user.save() 
        return user
    
    @staticmethod
    def get_user_by_id(id) -> Document: 
        return Users.objects.get(id=id)
    
    @staticmethod
    def list_users(): 
        users = Users.objects()
        return users
    
    @staticmethod
    def validate_query(payload) -> dict: 
        query = {}
        if "email" in payload: 
            query["email"] = payload["email"]
        if "name" in payload: 
            query["name"] = payload["name"]
        if "password" in payload: 
            query["password"] = payload["password"]
        return query
    
    
    