import sqlite3

class Database:
    _instance = None

    # @classmethod
    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(db_name)
        return cls._instance

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()
    
db = Database('app.db')

def save_username(username):
    db.execute_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    db.execute_query(f'INSERT INTO users (username) VALUES ("{username}")')

def save_weight(weight):
    db.execute_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    db.execute_query(f'INSERT INTO users (username) VALUES ("{weight}")')

def save_height(height):
    db.execute_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    db.execute_query(f'INSERT INTO users (username) VALUES ("{height}")')

def save_age(age):
    db.execute_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    db.execute_query(f'INSERT INTO users (username) VALUES ("{age}")')

def save_activity_time(activity_time):
    db.execute_query('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    db.execute_query(f'INSERT INTO users (username) VALUES ("{activity_time}")')

print(db1.execute_query('SELECT * FROM users'))
print(db2.execute_query('SELECT * FROM users'))