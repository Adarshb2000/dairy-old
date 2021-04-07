import sqlite3
import ast
# RE for converting normal statements to SQLite commands
import re
import itertools
from datetime import datetime
# Setting up database
conn = sqlite3.connect("database.db")
db = conn.cursor()

print(db.execute("SELECT * FROM Pregnancy").fetchall())