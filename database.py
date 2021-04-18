import sqlite3
import os

try:
    os.remove('database.db')
except FileNotFoundError:
    pass

conn = sqlite3.connect("database.db")
db = conn.cursor()

with conn:
    db.execute("""CREATE TABLE IF NOT EXISTS 'Cows' (
        'TagNumber' smallint PRIMARY KEY NOT NULL,
        'BoughtFrom' varchar(100) NOT NULL,
        'BoughtDate' date NOT NULL DEFAULT CURRENT_DATE,
        'VehicleNumber' smallint NOT NULL,
        'IsPregnant' boolean,
        'IsPregnantNotTested' boolean,
        'IsGivingMilk' boolean,
        'IsSick' boolean,
        'Comment' text
        )""")
    db.execute("""CREATE TABLE IF NOT EXISTS 'MilkHistory' (
        'TagNumber' integer NOT NULL,
        'LineNumber' smallint NOT NULL,
        'Milk' NUMERIC NOT NULL,
        'MilkDate' date NOT NULL DEFAULT CURRENT_DATE,
        FOREIGN KEY(TagNumber) REFERENCES Cows(TagNumber)
        )""")
    db.execute("""CREATE TABLE IF NOT EXISTS 'Pregnancy' (
        'TagNumber' smallint NOT NULL,
        'UthiDate' date,
        'BullNumber' smallint (100),
        'TestDate' date,
        'DoctorName' varchar(100),
        'DoctorConfirm' boolean,
        'PregnancyStart' date,
        'MilkStop' date,
        'DeliveryDate' date,
        'Gender' boolean,
        FOREIGN KEY(TagNumber) REFERENCES Cows(TagNumber)
        )""")
    db.execute("""CREATE TABLE IF NOT EXISTS 'Diseases' (
        'TagNumber' integer NOT NULL,
        'DiseaseID' integer NOT NULL,
        'Vaccine' varchar(100) NOT NULL,
        'DiseaseDoctor' varchar(100) NOT NULL,
        'VaccineDate' date NOT NULL,
        FOREIGN KEY(TagNumber) REFERENCES Cows(TagNumber)
        )""")