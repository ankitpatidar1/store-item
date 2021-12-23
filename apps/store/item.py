from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request

from apps.store.models import ItemModel
from apps.store.schema import ItemSchema
import sqlite3

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)
item_instance_schema = ItemSchema(load_instance=True)

class Item(Resource):

    # @jwt_required()
    def get(self,store_id,item_id):
        data = {"store_id":store_id,"item_id":item_id}
        row = ItemModel().fetch(**data)
        if row :
            return item_schema.dump(row) , 200
        else:
            return {"message": "item not match"} ,404

    def post(self,store_id):
        data = request.get_json()
        data.update({"store_id":store_id})
        item = item_instance_schema.load(data)
        item.insert()
        return item_schema.dump(item), 200

    def put(self,store_id,item_id):
        data = request.get_json()
        data.update({"store_id":store_id})
        item_instance = item_instance_schema.load(data)
        row = ItemModel().fetch(store_id=store_id,item_id=item_id)
        if row:
            row.name = item_instance.name
            row.price = item_instance.price 
        else:
            row = item_instance
        row.insert()
        return item_schema.dump(row), 200
    
    def delete(self,store_id,item_id):
        row = ItemModel().fetch(store_id=store_id,item_id=item_id)
        if row:
            msg = row.delete()        
            return {'status': msg}, 200
        return {'status': "store not found"}, 400

class ItemList(Resource):
    def get(self):
        rows = ItemModel().fetch()
        return {"items": item_list_schema.dump(rows)}
