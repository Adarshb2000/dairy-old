from flask import Flask, redirect, render_template, request
import sqlite3
import ast

# RE for converting normal statements to SQLite commands
import re

from helpers import get_milk_history

# Setting up database
conn = sqlite3.connect("testdb.db", check_same_thread=False)
db = conn.cursor()
# For rows
"""with conn:
    conn.row_factory = lambda cursor, row: row[0]
    db_row = conn.cursor()"""

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    # Getting all the variables
    tag = request.form.get("tag")
    bought_from = request.form.get("bought_from")
    milk_history = request.form.get("milk_history")
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

    milk_history_table = dict()
    if milk_history:
        milk_history_date0 = request.form.get('milk_history_date0')
        milk_history_date1 = request.form.get('milk_history_date1')

        print(milk_history_date0, milk_history_date1)

        # Selecting the cows where tag_condition is 1 if user hasn't given any
        cows_info = db.execute("SELECT * FROM cows WHERE " + condition).fetchall()

        # Getting the last two information of all the cows
        for cow_info in cows_info:
            milk_dict = ast.literal_eval(cow_info[2])
            new_milk_history = [(ln, date, milk) for milk, (ln, date) in milk_dict]
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
        
    return condition

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    
    # Getting all the variables
    tag = int(request.form.get("tag"))
    bought_from = request.form.get("bought_from")

    # For Milk History
    milk_history = get_milk_history(request.form.get("milk_history"))

    with conn:
        db.execute(f"INSERT INTO cows ('tag','bought_from', 'milk_history') VALUES (:tag, :bought_from, :new_milk_history)",
                    {
                        'tag': tag,
                        'bought_from': bought_from,
                        'new_milk_history': str(milk_history)
                    })

    return redirect('/add')

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        return render_template("update.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        return render_template("delete.html")
