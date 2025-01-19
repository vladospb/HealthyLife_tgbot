import sqlite3

class Database_food:
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

def log_food(id, food, amount, calories):
    db = Database_food('foods.db')
    db.execute_query("""CREATE TABLE IF NOT EXISTS foods (
    tg_id TEXT NOT NULL,
    food TEXT,
    amount TEXT,
    calories TEXT
    )""")
    db.execute_query(f'INSERT INTO foods (tg_id, food, amount, calories) VALUES ({f"'{id}'"}, {f"'{food}'"}, {f"'{amount}'"}, {f"'{calories}'"})')
    print(db.execute_query('SELECT * FROM foods'))

log_food('4', 'banana', '200', '800')