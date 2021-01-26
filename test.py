import sqlite3
from datetime import datetime

conn = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
db = conn.cursor()
values = ('137', '1', 1, datetime.date(datetime.strptime('2020-12-20', '%Y-%m-%d')))


# db.execute("INSERT INTO 'MilkHistory' ('TagNumber', 'LineNumber', 'Milk', 'MilkDate') VALUES (" + ', '.join(tuple(['?'] * len(values))) + ')', values)

print(db.execute("SELECT * FROM Cows").fetchall())
print(db.execute("SELECT * FROM MilkHistory").fetchall())
print(db.execute("SELECT * FROM Pregnancy").fetchall())
