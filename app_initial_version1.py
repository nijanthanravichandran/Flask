from flask import Flask, request
from db import stores, items

# app = Flask(__name__)
app=None

@app.route('/')
def index():
    return "Hello, World!"


@app.get("/store")
def get_stores():
    return {"stores ": stores}


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return {"store":store}
    return "store not exist", 400

@app.get("/store/<string:name>/items")
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items" : store["items"]}
    return "store not exist", 400


@app.post("/store")
def add_store():
    request_data = request.get_json()
    for store in stores:
        if store["name"] == request_data["name"]:
            return "store already exist"
    new_store = { "name" : request_data["name"], "items": request_data["items"]}
    stores.append(new_store)
    return new_store, 201

@app.post("/store/<string:name>/item")
def add_store_items(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            for item in request_data:
                new_item = {"name" : item["name"], "price": item["price"]}
                store["items"].append(new_item)
            return {"store" : store},200
    return "store not found", 404

    
    