import sys
import os
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import time
import csv

##--------------------------------------------------------------
## ------ START Pull today's temperature 40 years ago
##--------------------------------------------------------------
# round current time to the hour
now = datetime.now()
#today_40ys = now - relativedelta(years=40)
today_40ys = now - relativedelta(years=40)
def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))
print(now)
print(hour_rounder(now))

dt = datetime.now()
today_date = dt.strftime('%x')
today_date_40ys = '{0.month}/{0.day}/{0.year}'.format(today_40ys)
print ("today is: " + today_date)
print ("40ys ago was: " + today_date_40ys)
today_time = hour_rounder(now).strftime("%H:%M:%S") 
print ("now is: " + today_time)
import csv
with open('40ysweather.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        date = row[1]
        time = row[2]
        temperature = row[6]
       
        if date == today_date_40ys and time == today_time:
            print("FOUND!")
            temperature_40ys = temperature
            print("40 years ago was: " + temperature + " degrees")
            exit()
                  
##--------------------------------------------------------------
## ------ END Pull today's temperature 40 years ago
##--------------------------------------------------------------




