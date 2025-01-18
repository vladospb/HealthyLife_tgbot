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

def save_profile(id, username, weight, height, age, workout_time, city):
    db = Database('app.db')
    db.execute_query("""CREATE TABLE IF NOT EXISTS users (
    tg_id TEXT NOT NULL,
    username TEXT,
    weight TEXT,
    height TEXT,
    age TEXT,
    workout_time TEXT,
    city TEXT
    )""")
    db.execute_query(f'INSERT INTO users (tg_id, username, weight, height, age, workout_time, city) VALUES ({id}, {username}, {weight}, {height}, {age}, {workout_time}, {city})')
    print(db.execute_query('SELECT * FROM users'))