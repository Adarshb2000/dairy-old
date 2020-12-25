from datetime import datetime, timedelta
from dateutil.relativedelta import *

date_string = '2020-12-20'

x = datetime.date(datetime.strptime(date_string, '%Y-%m-%d'))

x = x - relativedelta(months=2.5)


print(x)