import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password='',
            database = 'fletapp'
        )
        if connection.is_connected():
            print('Connected')
            return connection
    except Error as e:
        print("Ahhh")
        return None
