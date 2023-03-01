import sqlite3 as sql
from sqlite3 import Error as e
class SqlDBQuery:
    def __init__(self):
        self.connect = sql.connect('student.db',timeout=130) 
        self.cursor = self.connect.cursor()


    def get_query(self,query,index=None):
        if index:
            self.cursor.execute(query,index)
            return self.cursor.fetchall()
        else:
            self.cursor.execute(query)
            return self.cursor.fetchall()
    
    def put_query(self,query,values):
        self.cursor.execute(query,values)
        
    def delete_query(self,query,index):
        self.cursor.execute(query,index)
        self.connect.commit()
        
    def __del__(self):
        self.connect.commit()
        self.connect.close()

    