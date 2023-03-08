import uuid
from flask_smorest import Blueprint, abort
from flask import request
from flask.views import MethodView
# from db import stores, items
from .schemas import ItemSchema
from models.item import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required


blb = Blueprint("items", __name__, description = "Opertion on items")


@blb.route("/item")
class ItemList(MethodView):
    
    @jwt_required()
    @blb.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required()
    @blb.arguments(ItemSchema)
    @blb.response(200, ItemSchema)
    def post(self, item_data):
            item = ItemModel(**item_data)
            try:
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message ="error in creating item")
            return item
    

@blb.route("/item/<string:item_id>")
class Item(MethodView):
    
    @jwt_required()
    @blb.arguments(ItemSchema)
    @blb.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel().query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
            item.store_id = item_data["store_id"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
        return item
    
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item deleted"}
    
    @jwt_required()
    @blb.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel().query.get_or_404(item_id)
        return item
