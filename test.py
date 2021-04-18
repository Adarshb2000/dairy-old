import sqlite3
from datetime import datetime
import os

os.remove('testdb.db')

conn = sqlite3.connect("testdb.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
db = conn.cursor()

db.execute("""CREATE TABLE IF NOT EXISTS 'Diseases' (
    'TagNumber' integer NOT NULL,
    'DiseaseID' integer NOT NULL,
    'Vaccine' varchar(100) NOT NULL,
    'DOCTOR' varchar(100) NOT NULL,
    'Date' date NOT NULL,
    FOREIGN KEY(TagNumber) REFERENCES Cows(TagNumber)
)""")
# values = ('137', '1', 1, datetime.date(datetime.strptime('2020-12-20', '%Y-%m-%d')))


# # db.execute("INSERT INTO 'MilkHistory' ('TagNumber', 'LineNumber', 'Milk', 'MilkDate') VALUES (" + ', '.join(tuple(['?'] * len(values))) + ')', values)

# print(db.execute("SELECT * FROM Cows").fetchall())
# print(db.execute("SELECT * FROM MilkHistory").fetchall())
# print(db.execute("SELECT * FROM Pregnancy").fetchall())
