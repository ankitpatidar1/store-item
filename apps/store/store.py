from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from data.app_database import UserDatabase
import sqlite3

items = [{"name": "ankit",}]

def get_filter(name,items):
    return next(filter(lambda item : item.get('name',None) == name ,items),None)

class Store(Resource):
    def get(self,store_id):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "SELECT * FROM store WHERE id=?"
        result = cursor.execute(cmd,(store_id,))
        row = result.fetchone()
        if row:
            return {"store":{"name":row[1]}},200
        else:
            return {"message": "item not match"},404

        UserDatabase.close_cursor(connection)

    def post(self):
        data = request.get_json()
        values = list(data.values())
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "insert into store(name) values(?)"
        cursor.execute(cmd, (*values,))
        UserDatabase.close_cursor(connection)
        return {'status': 'store item created successfully'}, 200

    def put(self,store_id):
        data = request.get_json()
        values = list(data.values())
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "update store set name=? where id=?"
        cursor.execute(cmd, (*values, store_id))
        UserDatabase.close_cursor(connection)
        return  {'status':'updated successfully'}, 200
        
    def delete(self,store_id):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "DELETE FROM store WHERE id=?"
        cursor.execute(cmd, (store_id,))
        UserDatabase.close_cursor(connection)
        return  {'status':'Deleted successfully'}, 200

class StoreList(Resource):
    def get(self):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "SELECT * FROM store"
        results = cursor.execute(cmd)
        rows = results.fetchall()
        return {"stores": list(map(lambda row:{"id": row[0],"name":row[1]},rows))}

class storeItem(Resource):
    def get(self,store_id):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "SELECT * FROM item where store_id=?"
        results = cursor.execute(cmd,(store_id,))
        rows = results.fetchall()
        return {
            "items": list(map(
                lambda row:{
                    "id": row[0],
                    "name":row[1], 
                    "price":row[2],
                    "store_id":row[3],
                    },rows)
            )
        }
