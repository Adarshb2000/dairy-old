from datetime import datetime
names = [("Adarsh", "Baderia"), ("Soumya", "Agrawal"), ("Ishita", "Nigam"), ("Akshat", "Bajpai")]
birthdays = ["20/05/2000", "16/09/2000", "25/10/2000", "01/07/2000"]

somethings = ["5", "6", "8", "1"]
"""names = { fname : lname for (fname, lname) in names }

for key, value in sorted(names.items(), key= lambda name: name[1], reverse=True):
    print(key, value, sep='|')"""
names_and_birthdays = list()

for name, something in zip(names, birthdays):
    names_and_birthdays.append((name[0], name[1], something))

old = [name_and_birthday for name_and_birthday in names_and_birthdays if datetime.strptime(name_and_birthday[2], '%d/%m/%Y') > datetime.strptime('20/05/2000', '%d/%m/%Y')]

print(old)

x = ["20/05/2000", "16/09/2000"]

y = [a for a in x if datetime.strptime(a, '%d/%m/%Y') >= datetime.strptime('20/05/2000', '%d/%m/%Y') and datetime.strptime(a, '%d/%m/%Y') < datetime.strptime('16/10/2000', '%d/%m/%Y')]

print(y)