import sqlite3
from db import db
from data.app_database import UserDatabase 

class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self,data={}):
        for key, value in data.items():
            setattr(self,key,value)

    def find_by_name(self,name):
        return self.__class__.query.filter_by(name=name).first()
        
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return "store saved successfully"
    
    def fetch(self,store_id=None):
        query = self.__class__.query        
        if store_id:
            return query.filter_by(id=store_id).first()
        else:
            return query.all()
        
    def delete(self):
        db.session.delete(self)
        msg = db.session.commit()
        return "store deleted successfully"

class ItemModel(db.Model):
    __tablename__='item'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    store_id = db.Column(db.Integer,db.ForeignKey('store.id'))

    def __init__(self,data={}):
        for key, value in data.items():
            setattr(self,key,value)

    @classmethod
    def find_by_name(cls,name):
        row = cls.query.filter_by(name=name).first()
        if row:
            return row
        else:
            return "Item Not Found"

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return "item saved successfully"
    
    
    def fetch(self,store_id=None,item_id=None):
        query = self.__class__.query
        if store_id and item_id:
            return query.filter_by(store_id=store_id).filter_by(id=item_id).first()
        elif item_id:
            return query.filter_by(id=item_id).first()
        elif store_id:
            return query.filter_by(store_id=store_id).all()
        else:
            return query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return  'Item Deleted successfully'


        

        


