from flask import request
from functools import wraps 

def accept_payload(func): 
    @wraps(func)
    def wrapper(*args, **kwargs): 
        payload = request.json
        return func(payload, *args, **kwargs) 
    
    return wrapper