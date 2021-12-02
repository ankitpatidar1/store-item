import sqlite3
from data.app_database import UserDatabase

class User:
    def __init__(self,_id=0,username='',password=''):
        self.id = _id
        self.name = username
        self.password = password

    def create_row(self, username,password):
        cursor,connection  = UserDatabase.get_cursor()
        cmd = "insert into user(name, password) values(?,?)"
        cursor.execute(cmd, (username,password))
        UserDatabase.close_cursor(connection)

    
    def find_by_username(self, username):

        cursor,connection = UserDatabase.get_cursor()
        cmd = "SELECT * FROM user WHERE name=?"
        result = cursor.execute(cmd,(username,))
        row = result.fetchone()
        if row:
            user = User(*row)
        else:
            user = None
        UserDatabase.close_cursor(connection)    
        return user
    
    def find_by_id(self, id):
        cursor,connection = UserDatabase.get_cursor()
        cmd = "select * from user where id=?"
        result = cursor.execute(cmd,(id,))
        row = result.fetchone()
        if row:
            user = User(*row)
        else:
            user = None
        UserDatabase.close_cursor(cursor,connection)
        return user
        



    

