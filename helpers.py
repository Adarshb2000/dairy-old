def get_milk_history(milk_history):
    milk_history = milk_history.split('!')
    
    LN = milk_history[0].lstrip('_').split('_')
    dates = milk_history[1].lstrip('_').split('_')
    milks = milk_history[2].lstrip('_').split('_')

    new_milk_history = dict()
    for ln, date, milk in zip(LN, dates, milks):
        new_milk_history[int(milk)] = (int(ln), date)

    return new_milk_history
