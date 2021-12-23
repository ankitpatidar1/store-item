from flask_restful import Resource
from flask_jwt_extended import jwt_required , get_jwt ,get_jwt_identity
from flask import request
from apps.store.models import StoreModel , ItemModel
from data.app_database import UserDatabase
from apps.store.schema import StoreSchema , ItemSchema
import sqlite3

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)
store_instance_schema = StoreSchema(load_instance=True)


class Store(Resource):
    def get(self,store_id):
        row = StoreModel().fetch(store_id=store_id)
        if row:
            return {"store":store_schema.dump(row)},200
        else:
            return {"message": "item not match"},404

    @jwt_required(fresh=True)
    def post(self):
        data = request.get_json()
        store_instance = store_instance_schema.load(data)
        msg = store_instance.insert()
        return {'status': msg}, 200

    def put(self,store_id):
        data = request.get_json()
        store_instance = store_instance_schema.load(data)
        row = StoreModel().fetch(store_id=store_id)
        if row:
            row.name = store_instance.name
        else:
            row = store_instance
        msg = row.insert()
        return {'status': msg}, 200

    @jwt_required()
    def delete(self,store_id):
        claims = get_jwt()
        if not claims['is_admin']:
            return { 
                "message": "need admin previledges" 
                } ,401
        fetch_row = StoreModel().fetch(store_id=store_id)
        if fetch_row:
            msg = fetch_row.delete()     
            return {'status': msg}, 200
        return {'status': "store not found"}, 400


class StoreList(Resource):

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        rows = StoreModel().fetch()
        if user_id:
            return {"stores": store_list_schema(rows)}
        else:
            return {"stores": list(map(lambda row:{"name":row.name},rows)),
            "message": "please login to get more info"}


class storeItem(Resource):
    def get(self,store_id):
        rows = ItemModel().fetch(store_id=store_id)
        return {"items": ItemSchema(many=True).dump(rows)}
