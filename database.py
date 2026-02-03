import sqlite3
import random
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name='bot_database.db'):
        self.db_name = db_name
        self.conn = None
        
    async def connect(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
    async def init_db(self):
        await self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                user_code TEXT UNIQUE,
                balance REAL DEFAULT 0.0,
                mentor TEXT DEFAULT 'Отсутствует',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    async def get_or_create_user(self, user_id, username, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            return dict(user)
        
        user_code = f"USR{random.randint(10000, 99999)}"
        
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, user_code)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, user_code))
        
        self.conn.commit()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return dict(cursor.fetchone())
    
    async def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    async def update_balance(self, user_id, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (amount, user_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def update_mentor(self, user_id, mentor_name):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET mentor = ? WHERE user_id = ?', (mentor_name, user_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def update_username(self, user_id, new_username):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET username = ? WHERE user_id = ?', (new_username, user_id))
        self.conn.commit()
        return cursor.rowcount > 0

db = Database()

async def init_db():
    await db.init_db()

async def get_or_create_user(user_id, username, first_name, last_name):
    return await db.get_or_create_user(user_id, username, first_name, last_name)

async def get_user(user_id):
    return await db.get_user(user_id)

async def update_balance(user_id, amount):
    return await db.update_balance(user_id, amount)

async def update_mentor(user_id, mentor_name):
    return await db.update_mentor(user_id, mentor_name)

async def update_username(user_id, new_username):
    return await db.update_username(user_id, new_username)
