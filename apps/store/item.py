from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request

from apps.store.models import ItemModel
import sqlite3

class Item(Resource):

    # @jwt_required()


    def get(self,store_id,item_id):
        data = {"store_id":store_id,"item_id":item_id}
        row = ItemModel().fetch(**data)
        if row :
            return {
                "id":row.id,
                "name":row.name,
                "price":row.price,
                "store_id":row.store_id,
                } , 200
        else:
            return {"message": "item not match"} ,404



    def post(self,store_id):
        data = request.get_json()
        data.update({"store_id":store_id})
        msg = ItemModel(data=data).insert()
        return {'status': msg}, 200

    
    def put(self,store_id,item_id):
        data = request.get_json()
        row = ItemModel().fetch(store_id=store_id,item_id=item_id)
        if row:
            row.name = data.get('name',row.name)
            row.price = data.get('price',row.price)
        else:
            datd.update({"store_id":store_id})
            row = ItemModel(data=data)
        msg = row.insert()
        return {'status': msg}, 200
    
    def delete(self,store_id,item_id):
        row = ItemModel().fetch(store_id=store_id,item_id=item_id)
        if row:
            msg = row.delete()        
            return {'status': msg}, 200
        return {'status': "store not found"}, 400

class ItemList(Resource):
    def get(self):
        rows = ItemModel().fetch()
        return {
            "items": list(map(
                lambda row:{
                    "id": row.id,
                    "name":row.name, 
                    "price":row.price,
                    "store_id":row.store_id,
                    },rows)
            )
        }
