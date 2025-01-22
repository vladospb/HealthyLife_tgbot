import sqlite3

class Database_workout:
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

def log_workout(id, date, workout, amount, calories):
    print(id, date, workout, amount, calories)
    db = Database_workout('workout.db')
    db.execute_query("""CREATE TABLE IF NOT EXISTS workout (
    tg_id TEXT NOT NULL,
    date DATE,
    workout TEXT,
    amount REAL,
    calories REAL
    )""")
    db.execute_query(f'INSERT INTO workout (tg_id, date, workout, amount, calories) VALUES ({f"'{id}'"}, {f"'{date}'"}, {f"'{workout}'"}, {f"'{amount}'"}, {f"'{calories}'"})')
    print(db.execute_query('SELECT * FROM workout'))

def get_workout_calories(id, date):
    db = Database_workout('workout.db')
    result = db.execute_query('''
        SELECT SUM(calories)
        FROM workout
        WHERE tg_id = ? AND date = ?
    ''', (id, date))
    
    if result and result[0][0] is not None:
        return result[0][0]
    return 0