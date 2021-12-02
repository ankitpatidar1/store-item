import sqlite3

class UserDatabase:
    def __init__(self):
        pass
    @classmethod
    def get_cursor(cls,database_name='user.db'):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        return cursor, connection
    
    @classmethod
    def close_cursor(cls,connection):
        connection.commit()
        connection.close()
    
    @classmethod
    def excute_cmd(cls,connection,cmd):
        try:
            connection.excute(cmd)
        except:
            pass
    
