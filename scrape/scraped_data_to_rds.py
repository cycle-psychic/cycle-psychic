# Used to move any files that have been scraped without being sent to RDS
import os
import mysql.connector
import json
from datetime import datetime

# Connect to database
connection = mysql.connector.connect(
  host='cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com',
  user='cyclepsychic',
  password='CyclePsychic123',
  db='cyclepsychic')

cursor = connection.cursor()

# data is the folder containing the files to upload to RDS - change as needed
# Looping through all files in saved folder and committing each one.

for name in os.listdir('data'):
  # Assumes that data is in a folder in the same directory as this script is currently in. Change as needed
  file = open('./data/'+name)
  json_file = json.load(file)

  for station in json_file:
    vals = (station.get('address'), station.get('contract_name'), \
      station.get('name'), datetime.fromtimestamp(int(station.get('last_update'))/1000), station['position'].get('lng'), \
        station['position'].get('lat'), station.get('status'), station.get('available_bikes'), \
          station.get('bonus'), station.get('available_bike_stands'),\
            station.get('number'), station.get('bike_stands'), station.get('banking'))
    sql = "INSERT IGNORE INTO `all_station_info` (`address`, `contract_name`, `name`, `last_update`, `lng`, `lat`,`status`, `available_bikes`, `bonus`, `available_bike_stands`, `number`, `bike_stands`, `banking`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql, vals)
    connection.commit()

connection.close()
