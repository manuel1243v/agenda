import mysql.connector
from datetime import datetime


class DatabaseManager:
    """Clase para gestionar la conexión con MySQL."""
    def __init__(self, host="localhost", user="root", password="", database="agenda"):
        self.config = {"host": host, "user": user, "password": password, "database": database}
        self.connect()

    def connect(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None, fetch=False):
        self.cursor.execute(query, params or ())
        if fetch:
            return self.cursor.fetchall()
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


class BaseModel:
    """Clase base para CRUD de modelos."""
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def execute(self, query, params=None, fetch=False):
        return self.db_manager.execute_query(query, params, fetch)
