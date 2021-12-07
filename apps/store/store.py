from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from apps.store.models import StoreModel , ItemModel
from data.app_database import UserDatabase
import sqlite3


class Store(Resource):
    def get(self,store_id):
        row = StoreModel().fetch(store_id=store_id)
        if row:
            return {"store":{"name":row.name}},200
        else:
            return {"message": "item not match"},404

    def post(self):
        data = request.get_json()
        msg = StoreModel(data=data).insert()
        return {'status': msg}, 200

    def put(self,store_id):
        data = request.get_json()
        fetch_row = StoreModel().fetch(store_id=store_id)
        if fetch_row:
            fetch_row.name = data.get('name')
        else:
            fetch_row = StoreModel(data=data)
        msg = fetch_row.insert()
        return {'status': msg}, 200
        
    def delete(self,store_id):
        fetch_row = StoreModel().fetch(store_id=store_id)
        if fetch_row:
            msg = fetch_row.delete()     
            return {'status': msg}, 200
        return {'status': "store not found"}, 400


class StoreList(Resource):
    def get(self):
        rows = StoreModel().fetch()
        return {"stores": list(map(lambda row:{"id": row.id,"name":row.name},rows))}

class storeItem(Resource):
    def get(self,store_id):
        rows = ItemModel().fetch(store_id=store_id)
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
