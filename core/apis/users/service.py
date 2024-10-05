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
    def list_users(page: int, per_page: int): 
        users = [user.to_mongo().to_dict() for user in Users.objects().order_by('name').skip(per_page*(page-1)).limit(per_page)]
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
    
    @staticmethod
    def get_collection_len(): 
        return Users.objects().count() 
    
    