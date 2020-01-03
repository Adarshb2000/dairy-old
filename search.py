import sqlite3
import ast
# RE for converting normal statements to SQLite commands
import re
import itertools
from datetime import datetime
from helpers import month_val
# Setting up database
conn = sqlite3.connect("testdb.db")
db = conn.cursor()

some_condition = "1"

milk_history_table = dict()
info = db.execute("SELECT * FROM cows WHERE " + some_condition).fetchall()
s = input()

months_finder = "(january|jan|feb|februrary|march|april|may|june|july|august|sept|september|oct|october|nov|november|dec|december)"

months = re.findall(r"\b" + months_finder + r'\b', s, re.I)
dates = re.findall(r"\b\d{1,2}\b", s, re.I)
years = re.findall(r"((\b\d{4}\b)|(\b'\d{2}\b))", s, re.I)

dates_array = []

now = datetime.now()

for date, month, year in itertools.zip_longest(dates, months, years):
    if not date:
        date = 31
    if not month:
        month = 12
    if not year:
        year = datetime.strftime("%Y")

    
    

    


conn.close()