import sqlite3
from tkinter import messagebox


class ContactManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                family TEXT,
                phone INTEGER,
                mobile INTEGER,
                UNIQUE(name, family, phone, mobile) ON CONFLICT IGNORE
            )
            """
            cur.execute(query)

    def insert(self, name, family, phone, mobile):
        if not name or not family:
            return False

        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            query = "INSERT INTO contact VALUES (NULL,?,?,?,?)"
            cur.execute(query, (name, family, phone, mobile))

        return True

    def delete(self, contact_id):
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            query = "DELETE FROM contact WHERE id = ?"
            cur.execute(query, (contact_id,))

        return True

    def view(self):
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            query = "SELECT * FROM contact"
            cur.execute(query)
            rows = cur.fetchall()
            return rows

    def search(self, name="", family="", phone="", mobile=""):
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            query = "SELECT * FROM contact WHERE name=? OR family=? OR phone=? OR mobile=?"
            cur.execute(query, (name, family, phone, mobile))
            rows = cur.fetchall()
            return rows
