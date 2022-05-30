## - Time and Weather Dashboard -
## by Andrea Fusi - https://www.linkedin.com/in/andrea-fusi-me/

# This program is based on a modified version of the code from AbnormalDistributions shown below in credits.
# Raspberry Pi Zero 2W is the controller used for this code.
# 3-color 7.5 inches e-ink display is used for this code.

# v1.0
# Template draft
# Update texts to italian
# Added times for current location, Taipei time and US West time
# Added temperature from same day and time, 40 years ago. reference: openweathermap

# credits: AbnormalDistributions
# https://github.com/AbnormalDistributions/e_paper_weather_display

## CC license:
## This license allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. 
## The license allows for commercial use. If you remix, adapt, or build upon the material, you must license the modified material under identical terms.

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
icondir = os.path.join(picdir, 'icon')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

# Search lib folder for display driver modules
sys.path.append('lib')
from waveshare_epd import epd7in5b_V2
epd = epd7in5b_V2.EPD()

from datetime import datetime, timedelta, date
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import pytz
import requests
import textwrap

from dateutil.relativedelta import relativedelta
import csv

##--------------------------------------------------------------
## ------ START Pull today's temperature 40 years ago
##--------------------------------------------------------------
print("--- START Pulling 40ys temperatures ---")
# round current time to the hour
now = datetime.now()
#today_40ys = now - relativedelta(years=40)
today_40ys = now - relativedelta(years=40)
def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

dt = datetime.now()
today_date = dt.strftime('%x')
today_date_40ys = '{0.month}/{0.day}/{0.year}'.format(today_40ys)
print ("Today date is: " + today_date)
print ("Today date 40ys ago was: " + today_date_40ys)
today_time = hour_rounder(now).strftime("%H:%M:%S") 
print("Rounded time to hour is: " + today_time)
import csv
with open('40ysweather.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        date = row[1]
        time = row[2]
        temperature = row[6]
       
        if date == today_date_40ys and time == today_time:
            print("Found weather records from 40 years ago!")
            temperature_40ys = temperature
            print("40 years ago now was: " + temperature + " degrees")
            
print("--- END Pulling 40ys temperatures ---")                           
##--------------------------------------------------------------
## ------ END Pull today's temperature 40 years ago
##--------------------------------------------------------------

#import news
class News:
    def __init__(self):
        pass

    def update(self, api_id):
        self.news_list = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=it&apiKey=fe3d6fd9afe84391a766146779a46283").json()
        return self.news_list

    def selected_title(self):
        list_news = []
        if self.news_list["status"] == "ok":
            for i in range(len(self.news_list["articles"])):
                line = self.news_list["articles"][i]["title"]
                line = textwrap.wrap(line, width=30)
                list_news.append(line)
        else:
            list_news = ["Problema caricamento news"]
        return list_news

##--------------------------------------------------------------
## ------ START Pull time for different time zones
##--------------------------------------------------------------
print("--- START Getting time from different cities ---")  
## get Taipei time
dt_taipei = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%H:%M')
print("Current Time in Taipei now: ", dt_taipei)
## get SF time
dt_SF = datetime.now(pytz.timezone('America/Vancouver')).strftime('%H:%M')
print("Current Time in SF now: ", dt_SF)
## get local time
dt_localtime = datetime.now().strftime('%H:%M')
print("--- END Getting time from different cities ---")  
##--------------------------------------------------------------
## ------ END Pull time for different time zones
##--------------------------------------------------------------

## Display definitions below
# define funciton for writing image and sleeping for 5 min.
def write_to_screen(image, sleep_seconds):
    print('Writing to screen...')
    # Write to screen
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open the template
    screen_output_file = Image.open(os.path.join(picdir, image))
    screen_output_file_Other = Image.open(os.path.join(picdir, image))
    # Initialize the drawing context with template as background
    h_image.paste(screen_output_file, (0, 0))
    epd.init()
    epd.display(epd.getbuffer(screen_output_file),epd.getbuffer(screen_output_file_Other))
    # Sleep
    time.sleep(10)
    epd.sleep()
    print('Image printed to display successful.')
    time.sleep(sleep_seconds)

# define function for displaying error
def display_error(error_source):
    # Display an error
    print('Error in the', error_source, 'request.')
    # Initialize drawing
    error_image = Image.new('1', (epd.width, epd.height), 255)
    # Initialize the drawing
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source +' ERROR', font=font50, fill=black)
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font = font50, fill=black)
    # Save the error image
    error_image_file = 'error.png'
    error_image.save(os.path.join(picdir, error_image_file))
    # Close error image
    error_image.close()
    # Write error to screen 
    write_to_screen(error_image_file, 30)

# Set the fonts
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)
font40 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 40)
font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)
font60 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 60)
font100 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 100)
font140 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 140)
# Set the colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
red = 'rgb(255,0,0)'

# Initialize and clear screen
print("--- START Getting time from different cities ---")  
print('Initializing e-ink display and clearing screen...')
epd.init()
epd.Clear()

##--------------------------------------------------------------
## ------ START Pull weather data from openweathermap
##--------------------------------------------------------------

API_KEY = 'c279d51a43080f3b57ec85ea278a8524'
LOCATION = 'Florence'
LOCATION_SF = 'SF'
LOCATION_TAIPEI = 'TAIPEI'
LATITUDE = '43.66'
LATITUDE_SF = '37.8'
LATITUDE_TAIPEI = '25.10'
LONGITUDE = '11.19'
LONGITUDE_TAIPEI = '121.59'
LONGITUDE_SF = '122.41'
UNITS = 'metric'
CSV_OPTION = True # if csv_option == True, a weather data will be appended to 'record.csv'

        
## START Pull Location 1
##------------
BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall?' 
URL = BASE_URL + 'lat=' + LATITUDE + '&lon=' + LONGITUDE + '&units=' + UNITS + '&lang=it' + '&appid=' + API_KEY

while True:
    # Ensure there are no errors with connection
    error_connect = True
    while error_connect == True:
        try:
            # HTTP request
            print('Attempting to connect to OWM.')
            response = requests.get(URL)
            print('Connection to OWM successful.')
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            display_error('CONNECTION') 
    
    error = None
    while error == None:
        # Check status of code request
        if response.status_code == 200:
            print('Connection to Open Weather successful.')
            # get data in jason format
            data = response.json()
            
            # get current dict block
            current = data['current']
            # get current
            temp_current = current['temp']
            # get feels like
            feels_like = current['feels_like']
            # get humidity
            humidity = current['humidity']
            # get pressure
            wind = current['wind_speed']
            # get description
            weather = current['weather']
            report = weather[0]['description']
            # get icon url
            icon_code = weather[0]['icon']
            #icon_URL = 'http://openweathermap.org/img/wn/'+ icon_code +'@4x.png'
            
            # get daily dict block
            daily = data['daily']
            # get daily precip
            daily_precip_float = daily[0]['pop']
            #format daily precip
            daily_precip_percent = daily_precip_float * 100
            # get min and max temp
            daily_temp = daily[0]['temp']
            temp_max = daily_temp['max']
            temp_min = daily_temp['min']
            
            # Append weather data to CSV if csv_option == True
            if CSV_OPTION == True:
                # Get current year, month, date, and time
                current_year = datetime.now().strftime('%Y')
                current_month = datetime.now().strftime('%m')
                current_date = datetime.now().strftime('%d')
                current_time = datetime.now().strftime('%H:%M')
                #open the CSV and append weather data
                with open('records.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow([current_year, current_month, current_date, current_time,
                                     LOCATION,temp_current, feels_like, temp_max, temp_min,
                                     humidity, daily_precip_float, wind])
                print('Weather data appended to CSV.')
## END Pull Location 1

##------------     
##--------------------------------------------------------------
## ------ END Pull weather data from openweathermap
##--------------------------------------------------------------
            
##--------------------------------------------------------------
## ------ START - TEMPLATE and LAYOUT setup
##--------------------------------------------------------------         
 
            ## Location 1
            string_location = LOCATION
            string_temp_current = format(temp_current, '.0f') + u'\N{DEGREE SIGN}C'
            string_temp_current_40ys = temperature_40ys + u'\N{DEGREE SIGN}C'
            string_feels_like = 'Percepita: \n' + format(feels_like, '.0f') +  u'\N{DEGREE SIGN}C'
            string_humidity = 'Umidità \n' + str(humidity) + '%'
            string_wind = 'Vento \n' + format(wind, '.1f') + ' KMH'
            string_report = 'Adesso: \n' + report.title()
            string_temp_max = 'Max: ' + format(temp_max, '>.0f') + u'\N{DEGREE SIGN}C'
            string_temp_min = 'Min:  ' + format(temp_min, '>.0f') + u'\N{DEGREE SIGN}C'
            string_precip_percent = 'Precip: \n' + str(format(daily_precip_percent, '.0f'))  + '%'
            
            # Set error code to false
            error = False
                    
            '''
            print('Location:', LOCATION)
            print('Temperature:', format(temp_current, '.0f'), u'\N{DEGREE SIGN}F') 
            print('Feels Like:', format(feels_like, '.0f'), 'F') 
            print('Humidity:', humidity)
            print('Wind Speed:', format(wind_speed, '.1f'), 'MPH')
            print('Report:', report.title())
            
            print('High:', format(temp_max, '.0f'), 'F')
            print('Low:', format(temp_min, '.0f'), 'F')
            print('Probabilty of Precipitation: ' + str(format(daily_precip_percent, '.0f'))  + '%')
            '''    
        else:
            # Call function to display HTTP error
            display_error('HTTP')

    # Open template file
    template = Image.open(os.path.join(picdir, 'template.png'))
    # Initialize the drawing context with template as background
    draw = ImageDraw.Draw(template)
    
    ## Draw time box
    draw.text((325, 15), "Time", font=font30, fill=white)
    draw.text((345, 50), dt_localtime, font=font30, fill=white)
    
    draw.text((325, 110), "Taipei", font=font30, fill=white)
    draw.text((345, 145), dt_taipei, font=font30, fill=white)  
    
    draw.text((325, 205), "US West", font=font30, fill=white)
    draw.text((345, 240), dt_SF, font=font30, fill=white)
    
    #Draw temperature box
    draw.text((480, 5), string_temp_current, font=font60, fill=black)
    draw.text((625, 5), string_temp_max, font=font35, fill=black)
    draw.text((625, 40), string_temp_min, font=font35, fill=black)
        ## Draw 40ys weather
    draw.text((480, 80), string_temp_current_40ys, font=font60, fill=black)
    draw.text((695, 90), ' Oggi\n40 anni fa', font=font22, fill=black)
    #draw.text((537, 250), weather40ys, font = font30, fill=black)
        # Draw humidity 
    draw.text((480, 150), string_humidity, font=font18, fill=black)
    draw.text((625, 150), string_wind, font=font18, fill=black)
        
        # Paste weather the image
            ## Open icon file
    icon_file = icon_code + '.png' 
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (470, 200))
      
        ## Draw precipitation and report
    draw.text((650, 220), string_report, font=font22, fill=black)
    draw.text((650, 300), string_precip_percent, font=font22, fill=black)
    
        # Draw top right box
    draw.text((350, 420), "Pasqualetti Residence", font=font40, fill=white)
    
##--------------------------------------------------------------
## ------ END - TEMPLATE and LAYOUT setup
##--------------------------------------------------------------         
    
    ## Add a reminder to take out trash on Mon, Wed, Fri
    #weekday = datetime.today().weekday()
    #if weekday == 0 or weekday == 2 or weekday == 4:
    #    draw.rectangle((345, 13, 705, 55), fill =black)
    #    draw.text((355, 15), "!! Garbage Recycling !!", font=font35, fill=white)
 
## ------ Save image as png and push to display
##--------------------------------------------------------------   
    # Save the image for display as PNG
    screen_output_file = os.path.join(picdir, 'screen_output.png')
    template.save(screen_output_file)
    # Close the template file
    template.close()
    
    # Refresh clear screen to avoid burn-in at 3:00 AM
    if datetime.now().strftime('%H') == '03':
    	print('Clearning screen to avoid burn-in.')
    	epd.Clear()
    
    # Write to screen
    write_to_screen(screen_output_file, 30)
    exit()