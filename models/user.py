from db import db 

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String, unique=True, nullable = False)
    password = db.Column(db.String, unique=False, nullable = False)