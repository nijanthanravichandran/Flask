import uuid
from flask_smorest import Blueprint, abort
from flask import request
from flask.views import MethodView
# from db import stores, items
from .schemas import UserSchema
from models.user import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from blocklist import BLOCKLIST


blb = Blueprint("users", __name__, description = "Users for loggin")


@blb.route("/user")
class User(MethodView):
    
    @blb.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    @blb.arguments(UserSchema)
    @blb.response(200, UserSchema)
    def post(self, UserData):
        user = UserModel(
            name=UserData["name"],
            password=pbkdf2_sha256.hash(UserData["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error in creating user")
        return user
    
@blb.route("/user/<int:user_id>")
class User(MethodView):
    
    @blb.response(200, UserSchema)
    def get(self,user_id):
        return UserModel.query.get_or_404(user_id)
    
    @blb.arguments(UserSchema)
    @blb.response(200, UserSchema)
    def post(self, UserData, user_id):
        user = UserModel.query.get(user_id)
        if user:
            user.name = UserData["name"]
            user.password = pbkdf2_sha256.hash(UserData["password"])
        else:
            user = UserModel(
            id=user_id,
            name=UserData["name"],
            password=pbkdf2_sha256.hash(UserData["password"])
            )

        db.session.add(user)
        db.session.commit()
        return user
    
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message" : "user deleted"}
    

@blb.route("/login")
class UserLogin(MethodView):
    
    @blb.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.name == user_data["name"]
        ).first()
        print(user.password, user_data["password"])
        if user and pbkdf2_sha256.verify( user_data["password"], user.password):
            access_token = create_access_token(identity= user.id)
            return {"access_token":access_token}
        
        abort(401, message="Invalid credentials")
        

@blb.route("/logout")
class UserLogout(MethodView):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200