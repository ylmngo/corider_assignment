from mongoengine import Document, StringField, EmailField 

class Users(Document): 
    name = StringField(required=True)
    email = EmailField(required=True) 
    password = StringField(required=True) 

    meta = {'db-alias': 'user-db-alias', 'collection': 'users'}  

    @staticmethod
    def getById(id): 
        return Users.objects.get(id=id)