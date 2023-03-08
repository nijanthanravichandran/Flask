from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    
    
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)