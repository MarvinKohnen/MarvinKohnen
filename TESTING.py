import datetime
from datetime import date, timedelta
from influxdb_client.client.util import date_utils
from dateutil.tz import tzlocal


a = datetime.datetime.today()

numdays = 10
dateList = []
for x in range (0, numdays):
    dateList.append(a - datetime.timedelta(days = x))

adjDateList = []
for x in range (0, numdays):
    adjDateList.append(dateList[x].strftime('%d').lstrip('0') + '.' + dateList[x].strftime('%m').strip('0') + '.' + dateList[x].strftime('%y'))
b = adjDateList[1]


for i in dateList:
    x = i.astimezone(tzlocal())
    print(x)

# Calling now() function to return
# current datetime
d1 = datetime.datetime.now().astimezone()



