import sqlite3 as sql

con = sql.connect('typing-test.db')
cur = con.cursor()

# Create tables
cur.execute('''CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')

cur.execute('''CREATE TABLE records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    count INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                        REFERENCES users(user_id)
                )''')

con.commit()

con.close()