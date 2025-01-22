import sqlite3

class Database:
    _instance = None

    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(db_name)
        return cls._instance

    def __init__(self, db_name):
        if not hasattr(self, 'connection'):
            self.connection = sqlite3.connect(db_name)

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        self.connection.commit()
        return cursor.fetchall()

def save_profile(id, reg_date, username, weight, height, age, workout_time, city):
    db = Database('profiles.db')
    db.execute_query("""CREATE TABLE IF NOT EXISTS profiles (
    tg_id TEXT NOT NULL,
    reg_date DATE,
    username TEXT,
    weight INTEGER,
    height INTEGER,
    age INTEGER,
    workout_time REAL,
    city TEXT
    )""")
    db.execute_query(f'INSERT INTO profiles (tg_id, reg_date, username, weight, height, age, workout_time, city) VALUES ({f"'{id}'"}, {f"'{reg_date}'"}, {f"'{username}'"}, {f"'{weight}'"}, {f"'{height}'"}, {f"'{age}'"}, {f"'{workout_time}'"}, {f"'{city}'"})')
    print(db.execute_query('SELECT * FROM profiles'))

def get_profile_info(id):
    db = Database('profiles.db')
    result = db.execute_query('''
        SELECT weight, height, age, city
        FROM profiles
        WHERE tg_id = ?
        ''', (f'{id}',))
    
    if result and result is not None:
        return list(result[-1])
    return 0