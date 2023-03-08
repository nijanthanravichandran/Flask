
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from .schemas import StoreSchema, PlainStoreSchema
from models.store import StoreModel
from flask_jwt_extended import jwt_required



blb = Blueprint("stores", __name__, description="Operation on stores")

@blb.route("/store")
class StoreList(MethodView):
    
    @jwt_required()
    @blb.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blb.arguments(StoreSchema)
    @blb.response(200, StoreSchema)
    def post(self, store_data):
            store = StoreModel(**store_data)
            try:
                db.session.add(store)
                db.session.commit()
            except IntegrityError:
                abort(
                    400,
                    message="A store with that name already exist"
                )
            except SQLAlchemyError:
                abort(500, message="Error in creating store.")
            
            return store
        
@blb.route("/store/<string:store_id>")
class Store(MethodView):
    
    @jwt_required()
    @blb.response(200, StoreSchema)
    def get(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            return store
    
    @jwt_required()
    @blb.arguments(StoreSchema)
    @blb.response(200, StoreSchema)
    def put(self, store_data, store_id):
            store = StoreModel.query.get(store_id)
            
            if store:
                store.name = store_data["name"]
            else:
                store = StoreModel(id=store_id, **store_data)
            
            db.session.add(store)
            db.session.commit()
            return store
    
    @jwt_required()
    def delete(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
            return {"message" : "Store deleted"}