import sqlite3
from data.app_database import UserDatabase
from db import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self,data={}):
        for key, value in data.items():
            setattr(self,key,value)

    def create_row(self):
        db.session.add(self)
        db.session.commit()
        return "user added in database"

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch(cls,user_id=None):
        query = cls.query        
        if user_id:
            return query.filter_by(id=user_id).first()
        else:
            return query.all()


        



    

