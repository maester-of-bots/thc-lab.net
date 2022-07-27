import sqlite3

connection = sqlite3.connect('data/database.db')

with open('data/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
