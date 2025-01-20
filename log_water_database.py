import sqlite3

class Database_water:
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

def log_water(id, date, water_amount):
    db = Database_water('water.db')
    db.execute_query("""CREATE TABLE IF NOT EXISTS water (
    tg_id TEXT NOT NULL,
    date DATE,
    water_amount REAL
    )""")
    db.execute_query(f'INSERT INTO water (tg_id, date, water_amount) VALUES ({f"'{id}'"}, {f"'{date}'"}, {f"'{water_amount}'"})')
    print(db.execute_query('SELECT * FROM water'))

def get_water_amount(id, date):
    db = Database_water('water.db')
    result = db.execute_query('''
        SELECT SUM(water_amount)
        FROM water
        WHERE tg_id = ? AND date = ?
    ''', (id, date))
    
    if result and result[0][0] is not None:
        return result[0][0]
    return 0