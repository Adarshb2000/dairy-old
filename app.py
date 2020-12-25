from flask import Flask, redirect, render_template, request
import sqlite3
import ast
from datetime import datetime, date, timedelta
from dateutil.relativedelta import *
import pandas as pd
import numpy as np

# RE for converting normal statements to SQLite commands
import re

date_pattern = "%Y-%m-%d"

# Setting up database
conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()
# For rows
"""with conn:
    conn.row_factory = lambda cursor, row: row[0]
    db_row = conn.cursor()"""

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Columns
cows_columns = ['TagNumber', 'BoughtDate', 'BoughtFrom', 'VehicleNumber']
milk_history_columns = ['TagNumber', 'LineNumber', 'Milk', 'MilkDate']
pregnancy_columns = ['TagNumber', 'UthiDate', 'BullNumber', 'TestDate', 'DoctorName', 'DoctorConfirm', 'PregnancyStart', 'MilkStop', 'DeliveryDate', 'Gender']


# DateTime Format
datetime_format = '%Y-%m-%d'


# SQLite functions
def add_to_table(database, table, dictionay):
    dictionay = dict(dictionay)
    key = tuple(dictionay.keys())
    value = tuple(dictionay.values())

    with database:
        database.cursor().execute("INSERT INTO" + f" '{table}' " + str(key) + " VALUES " + str(value))



@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    
    # Getting all the variables
    animal = request.form.get('animal_category')
    
    # Cows table
    information_table = {column : request.form.get(column) for column in cows_columns}
    
    print(animal, information_table, sep='\n')

    # Milk History Table
    table = {column : request.form.getlist(column) for column in milk_history_columns}
    table['TagNumber'] *= len(table[milk_history_columns[1]])

    print(table)

    for values in zip(*table.values()):
        if '' in values:
            continue
        adding_dict = {milk_history_columns[i] : values[i] for i in range(len(values))}

        print(adding_dict)


    # Table Pregnancy
    table = {column : request.form.getlist(column) for column in pregnancy_columns}
    table['TagNumber'] *= len(table[pregnancy_columns[1]])

    print(table, '\n\n\n')

    # for TagNumber, UthiDate, UthiDetails, TestDate, DoctorName, DoctorConfirm, PregnancyStart, MilkStop, DeliveryDate, Gender in zip(*table.values()):
    for values in zip(*table.values()):

        values = list(values)

        if values == [''] * len(values): continue

        if values[1 : -2] == [''] * 7:
            adding_dict = {pregnancy_columns[i] : values[i] for i in range(len(values))}



        if not values[pregnancy_columns.index('TestDate')]:
            adding_dict = {pregnancy_columns[i] : values[i] for i in range(3)}
        
        
        
        else:
            values[pregnancy_columns.index('TestDate')] = TestDate = datetime.date(datetime.strptime(values[pregnancy_columns.index('TestDate')], datetime_format))
            values[pregnancy_columns.index('DoctorConfirm')] = x = int(values[pregnancy_columns.index('DoctorConfirm')])
            if not x:
                adding_dict = {pregnancy_columns[i] : values[i] for i in range(6)}
            else:
                x = float(values[pregnancy_columns.index('PregnancyStart')])
                values[pregnancy_columns.index('PregnancyStart')] = TestDate - relativedelta(month=int(x))
                if not x.is_integer(): values[pregnancy_columns.index('PregnancyStart')] - relativedelta(weeks=2)
                if values[-3]: values[-3] = datetime.date(datetime.strptime(values[-3], datetime_format))
                if values[-2]: values[-2] = datetime.date(datetime.strptime(values[-2], datetime_format))
                values[-1] = 1 if not values[-1] or values[-1] == '-1' else int(values[-1])
                
                adding_dict = {pregnancy_columns[i] : values[i] for i in range(len(values))}

        print(adding_dict)
    


    return redirect('/')


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    # Getting all the variables
    tag = request.form.get("tag")
    bought_from = request.form.get("bought_from")
    milk_history = request.form.get("milk_history")
    want_milk_history = request.form.get("want_milk_history")
    #pregnancy = request.form.get("pregnancy")
    #diseases = request.form.get("diseases")
    #comment = request.form.get("comment")

    condition = ""

    tag_condition = ""
    if tag:
        tag_matches = re.findall(r'\b\d{1,3}\b', tag)
        if not tag_matches:
            return render_template("search.html")
        if len(tag_matches) == 2:
            if len(re.findall(r'(between|among)', tag)):
                tag_condition = f"tag BETWEEN '{sorted(tag_matches)[0]}' AND '{sorted(tag_matches)[1]}'"
            else:
                tag_condition = f"tag='{tag_matches[0]}' OR tag='{tag_matches[1]}'"
        elif len(tag_matches) > 2:
            for tag_number in tag_matches:
                tag_condition += f"tag='{tag_number}' OR "
            tag_condition = tag_condition.rstrip(" OR ")
        else:
            tag_condition = f"tag='{tag_matches[0]}'"
    else:
        tag_condition = "1"
    tag_condition += " AND "
    
    condition = tag_condition

    bought_from_condition = ""
    if bought_from:
        bought_from_condition = f"bought_from = '{bought_from}'"
    else:
        bought_from_condition = "1"
    #bought_from_condition += " AND " FOR_NOW

    condition += bought_from_condition

    milk_table = dict()
    if milk_history or want_milk_history:
        milk_history_start_date = request.form.get('milk_history_start_date') 
        milk_history_end_date = request.form.get('milk_history_end_date')

        #if not milk_history_start_date:
            #milk_history_start_date = str(datetime.strptime("0001-01-01", date_pattern))
        #if not milk_history_end_date:
            #milk_history_end_date = str(date.today())


        # Selecting the cows where tag_condition is 1 if user hasn't given any
        cows_info = db.execute("SELECT * FROM cows WHERE " + condition).fetchall()
        milk_history_table = dict()

        # Getting the last two information of all the cows
        for cow_info in cows_info:
            milk_dict = ast.literal_eval(cow_info[2])
            new_milk_history = [(ln, date, milk) for milk, (ln, date) in milk_dict.items() if datetime.strptime(date, date_pattern) >= datetime.strptime(milk_history_start_date, date_pattern) and datetime.strptime(date, date_pattern) <= datetime.strptime(milk_history_end_date, date_pattern)]
            milk_history_table[cow_info[0]] = [new_milk for new_milk in new_milk_history]

        # Searching for words
        if re.findall(r'(max(imum)?|high(est)?|most|great(est)?)', milk_history, re.I):
            milk_table = sorted(milk_history_table.items(), key=lambda item: item[1][0][2], reverse=True)

        elif re.findall(r'(more( than)?|above|higher|greater)', milk_history, re.I):
            milk_table = { tag : info for tag, info in sorted(milk_history_table.items(), key=lambda item: item[1][0][2], reverse=True) if (info[0][2] > int(re.findall(r'(\b\d{1,2}\b)', milk_history)[0]))}

        elif re.findall(r'less( than)?(er)?|below|lower', milk_history, re.I):
            milk_table = { tag : info for tag, info in sorted(milk_history_table.items(), key=lambda item: item[1][0][2], reverse=True) if (info[0][2] < int(re.findall(r'(\b\d{1,2}\b)', milk_history)[0]))}
        else:
            milk_table = milk_history_table
        
    return f"{milk_table}"





@app.route("/add1", methods=["GET", "POST"])
def add1():
    if request.method == "GET":
        return render_template("add1.html")



@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        return render_template("update.html")


@app.route('/temp', methods=["GET", "POST"])
def temp():
    if request.method == "GET":
        return render_template('temp.html')
    else:
        date_ = request.form.get('something')
        print(datetime.date(datetime.strptime(date_, "%Y-%m-%d")))

        return redirect('/temp')



if __name__ == "__main__":
    app.run('192.168.29.62', debug=True)