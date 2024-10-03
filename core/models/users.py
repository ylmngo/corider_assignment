from pydantic import BaseModel, Field
from typing import Optional, Annotated
from bson import ObjectId
from .objectid import ObjectIdPydanticAnnotation


class UserIn(BaseModel): 
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(None, alias="_id")
    name: str 
    email: str 
    password: str

    def to_json(self): 
        return self.model_dump(mode="json", exclude={"password"})
    
    def to_bson(self): 
        data = self.model_dump(mode="python", by_alias=True, exclude=None)
        if data["_id"] is None: 
            data.pop("_id")
        return data 
        
class UserOut(BaseModel): 
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(None, alias="_id")
    name: str 
    email: str 

    def to_json(self): 
        return self.model_dump(mode="json") 
    
    def to_bson(self): 
        data = self.model_dump(mode="python", by_alias=True, exclude=None) 
        return data 
    

class UserUpdate(BaseModel): 
    name: Optional[str] = None 
    email: Optional[str] = None
    password: Optional[str] = None

    def to_json(self): 
        return self.model_dump(mode="json")
    
    def to_bson(self): 
        data = self.model_dump(mode="python", by_alias=True, exclude=None)
        return data 