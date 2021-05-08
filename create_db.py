import sqlite3

connection = sqlite3.connect('patterns.sqlite')
cur = connection.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
connection.close()
