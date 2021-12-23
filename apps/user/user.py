import sqlite3
from requests import Response ,post
from flask import request , url_for
from data.app_database import UserDatabase
from mailgun import Mailgun
from db import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False, unique=True)
    activated = db.Column(db.Boolean,default=False)
    
    def create_row(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        
    def send_confirmation(self) -> Response:
        # send  user confirmation mail
        link = request.url_root[:-1] + url_for("userconfirm",user_id=self.id)
        title = "Store REST API"
        subject = "User Confirmation Mail"
        html_str = '<html><body>Please click on link for confirmation for your registration <a href="%s">link</a> </body></html>' % link
        to_mail = "apexankitpatidar@gmail.com"
        Mailgun.send_confirmation(title,to_mail,subject,html_str)

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


        



    

