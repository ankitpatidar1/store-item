from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from data.app_database import UserDatabase
import sqlite3

class Item(Resource):
    # @jwt_required()
    def get(self,store_id,item_id):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "SELECT * FROM item WHERE store_id=? AND id=?"
        result = cursor.execute(cmd,(store_id,item_id))
        row = result.fetchone()
        print(row)
        if row:
            return {"item":{"name":row[1],"price":row[2],"store":row[3]}},200
        else:
            return {"message": "item not match"},404

        UserDatabase.close_cursor(connection)
        

    def post(self,store_id):
        data = request.get_json()
        values = list(data.values())
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "insert into item(name, price,store_id) values(?,?,?)"
        cursor.execute(cmd, (*values,store_id))
        UserDatabase.close_cursor(connection)
        return {'status': 'item saved successfully'}, 200

    
    def put(self,store_id,item_id):
        data = request.get_json()
        values = list(data.values())
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "update item set name=?, price=? where store_id=? and id=?"
        cursor.execute(cmd, (*values, store_id,item_id))
        UserDatabase.close_cursor(connection)
        return  {'status':'Item updated successfully'}, 200
    
    def delete(self,store_id,item_id):        
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "DELETE FROM item WHERE store_id=? AND id=?"
        cursor.execute(cmd, (store_id,item_id))
        UserDatabase.close_cursor(connection)
        return  {'status':'Deleted successfully'}, 200
        

class ItemList(Resource):
    def get(self):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "SELECT * FROM item"
        results = cursor.execute(cmd)
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
