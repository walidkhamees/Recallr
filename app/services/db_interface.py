import sqlite3

class DB_interface:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def close(self):
        self.conn.close()

    def execute(self, query: str, params: tuple = ()):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur
    
    def rollback(self):
        self.conn.rollback()

    def execute_without_commit(self, query: str, params: tuple = ()):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(query, params)
        return cur

    def commit(self):
        self.conn.commit()


    def fetch_all(self, query: str, params: tuple = ()):
        cur = self.execute(query, params)
        return cur.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        cur = self.execute(query, params)
        return cur.fetchone()
