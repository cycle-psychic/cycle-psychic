# Used to move any files that have been scraped without being sent to RDS
import os
import mysql.connector
import json
from datetime import datetime

# Connect to database
connection = mysql.connector.connect(
  host='cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com',
  user='cyclepsychic',
  password='putpasswordhere',
  db='cyclepsychic')

cursor = connection.cursor()

# 'weather' is the folder containing the files to upload to RDS - change as needed
# Looping through all files in saved folder and committing each one.

for name in os.listdir('weather'):
  # Assumes that data is in a folder in the same directory as this script is currently in. Change as needed
  file = open('./weather/'+name)
  data = json.load(file)

  #assign data in the JSON file to variables
  coord_lon = data["coord"]["lon"]  #longitude in db
  coord_lat = data["coord"]["lat"]  #latitude in db

  base = data["base"]

  main_temp = data["main"]["temp"]
  main_pressure = data["main"]["pressure"]
  main_humidity = data["main"]["humidity"]
  main_temp_min = data["main"]["temp_min"]
  main_temp_max = data["main"]["temp_max"]
  # sea_level may not be in the JSON file
  if "sea_level" in data["main"]:
    main_sea_level = data["main"]["sea_level"]
  else:
    main_sea_level = 'NULL'
  # grnd_level may not be in the JSON file
  if "grnd_level" in data["main"]:
    main_grnd_level = data["main"]["grnd_level"]
  else:
    main_grnd_level = 'NULL'

  # wind data may not be in the JSON file
  if "wind" in data:
    if "speed" in data["wind"]:
      wind_speed = data["wind"]["speed"]  #main_wind_speed in db
    else:
      wind_speed = 'NULL'
    if "deg" in data["wind"]:
      wind_deg = data["wind"]["deg"]  #main_wind_direction in db
    else:
      wind_deg = 'NULL'
  else:
    wind_speed = 'NULL'
    wind_deg = 'NULL'

  # cloud data may not be in the JSON file
  if "clouds" in data:
    if "all" in data["clouds"]:
      clouds_all = data["clouds"]["all"]  #main_clouds in db
    else:
      clouds_all = 'NULL'

  # rain data may not be in the JSON file
  if "rain" in data:
    if "1h" in data["rain"]:
      rain_1h = data["rain"]["1h"]  #main_rain_volume_1h in db
    else:
      rain_1h = 'NULL'
    if "3h" in data["rain"]:
      rain_3h = data["rain"]["3h"]  #main_rain_volume_3h in db
    else: 
      rain_3h = 'NULL'
  else:
    rain_1h = 'NULL'
    rain_3h = 'NULL'

  # snow data may not be in the JSON file
  if "snow" in data:
    if "1h" in data["snow"]:
      snow_1h = data["snow"]["1h"]  #main_snow_volume_1h in db
    else:
      snow_1h = 'NULL'
    if "3h" in data["snow"]:
      snow_3h = data["snow"]["3h"]  #main_snow_volume_3h in db
    else:
      snow_3h = 'NULL'
  else:
    snow_1h = 'NULL'
    snow_3h = 'NULL'

  dt = data["dt"]  #last_update in db

  sys_type = data["sys"]["type"]
  sys_id = data["sys"]["id"]
  sys_message = data["sys"]["message"]
  sys_country = data["sys"]["country"]
  sys_sunrise = data["sys"]["sunrise"]
  sys_sunset = data["sys"]["sunset"]

  id = data["id"]  #city_id in db
  name = data["name"]  #city_name in db
  cod = data["cod"]
  
  for weather in data["weather"]:
    weather_id = weather.get("id")
    weather_main = weather.get("main")
    weather_description = weather.get("description")
    weather_icon = weather.get("icon")

    # values that will be inserted into the database
    vals = (coord_lon, coord_lat, base, main_temp, main_pressure, main_humidity, main_temp_min, \
      main_temp_max, main_sea_level, main_grnd_level, wind_speed, wind_deg, clouds_all, rain_1h, \
      rain_3h, snow_1h, snow_3h, datetime.fromtimestamp(int(dt)), sys_type, sys_id, sys_message, sys_country, \
      datetime.fromtimestamp(int(sys_sunrise)), datetime.fromtimestamp(int(sys_sunset)), id, name, cod, \
      weather_id, weather_main, weather_description, weather_icon)

    #sql insert command
    sql = "INSERT IGNORE INTO `city_weather` (`longitude`, `latitude`, `base`, `main_temp`, \
      `main_pressure`, `main_humidity`, `main_temp_min`, `main_temp_max`, `main_sea_level`, \
      `main_grnd_level`, `main_wind_speed`, `main_wind_direction`, `main_clouds`, `main_rain_volume_1h`, \
      `main_rain_volume_3h`, `main_snow_volume_1h`, `main_snow_volume_3h`, `last_update`, `sys_type`, \
      `sys_id`, `sys_message`, `sys_country`, `sys_sunrise`, `sys_sunset`, `city_id`, `city_name`, \
      `cod`, `weather_id`, `weather_main`, `weather_description`, `weather_icon`) \
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql, vals)

    #commit each command
    connection.commit()
    #close the file
    file.close()

#close db connection
connection.close()