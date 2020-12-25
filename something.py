import sqlite3

conn = sqlite3.connect("testdb.db")
db = conn.cursor()

with conn:
    db.execute("DROP TABLE cows")