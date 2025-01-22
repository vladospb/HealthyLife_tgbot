import sqlite3

class Database_food:
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



def log_food(id, date, food, amount, calories):
    db = Database_food('foods.db')
    db.execute_query("""CREATE TABLE IF NOT EXISTS foods (
    tg_id TEXT NOT NULL,
    date DATE,
    food TEXT,
    amount REAL,
    calories REAL
    )""")
    db.execute_query(f'INSERT INTO foods (tg_id, date, food, amount, calories) VALUES ({f"'{id}'"}, {f"'{date}'"}, {f"'{food}'"}, {f"'{amount}'"}, {f"'{calories}'"})')
    print(db.execute_query('SELECT * FROM foods'))



def get_food_calories(id, date):
    db = Database_food('foods.db')
    result = db.execute_query('''
        SELECT SUM(calories)
        FROM foods
        WHERE tg_id = ? AND date = ?
    ''', (id, date))
    
    if result and result[0][0] is not None:
        return result[0][0]
    return 0