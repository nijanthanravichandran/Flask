# Additional end points
# Validation for payload



from flask import Flask, request
from db import stores, items
import uuid
from flask_smorest import abort

# app = Flask(__name__)
app=None

@app.get("/store")
def get_stores():
    return stores


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message ="Store not found" )


@app.post("/store")
def add_store():
    store_data = request.get_json()
    
    if ("name" not in store_data):
        abort(400, message= "name must be there in json payload")
        
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(404, message="store already exist")
    
    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store

@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    
    if ("name" not in store_data):
        abort(400, message= "name must be there in json payload")
        
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message" : "Item deleteed."}
    except KeyError:
        abort(404, message= "key not found")

    
@app.get("/item/")
def get_store_items():
    return items


@app.get("/item/<string:item_id>")
def get_store_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


@app.post("/item")
def add_store_items():
    item_data = request.get_json()
    
    if("name" not in item_data or "store_id" not in item_data or "price" not in item_data):
        abort(400, message="Ensure namne, store_id & price in Json payload")
    
    if item_data["store_id"] not in stores:
        return {"message" : "store not found"},404
    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item
    return item

@app.put("/item/<string:item_id>")
def update_store_items(item_id):
    item_data = request.get_json()
    
    if("name" not in item_data or "store_id" not in item_data or "price" not in item_data):
        abort(400, message="Ensure namne, store_id & price in Json payload")
    
    if item_data["store_id"] not in stores:
        return {"message" : "store not founc"},404
    item = {**item_data, "id":item_id}
    items[item_id] = item
    return item

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item Deleted"}
    except KeyError:
        abort(404, message="Item not found")