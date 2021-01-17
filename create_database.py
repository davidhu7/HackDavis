import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

sql = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    );
"""
cur.executescript(sql)

sql = """
INSERT INTO users (username, password) values
    ('brandon', 'nice'),
    ('david', 'great'),
    ('kotaro', 'handsome'),
    ('rojan', 'spices')
"""
cur.executescript(sql)
con.commit()
