# db.py

import sqlite3
import bcrypt

DATABASE = "app.db"

def get_connection():
    return sqlite3.connect(DATABASE)