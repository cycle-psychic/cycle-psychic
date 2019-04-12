
import json
import mysql.connector
import requests
""" This script accessed JCDeceaux to fill the station_data table in SQL with static information that is not updated"""

# retrieve bike station information
api_key= "6313dca4b06d3b5a526328199f9abe54c817b512"
api_endpoint = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api_key

# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
    )

r = requests.get(url=api_endpoint)

# send request and store in json
bike_stations = r.json()

# prepare to execute statements
cursor = dbEngine.cursor()

# place the results into the DB station_information table
for station in bike_stations:
  vals = (station.get('number'), station.get('contract_name'), station.get('name'),\
          station.get('address'), station['position'].get('lat'),\
          station['position'].get('lng'),station.get('bike_stands'), station.get('banking'))
  sql = "INSERT IGNORE INTO `station_information` (`station_number`, `contract_name`, `name`, `address`, `latitude`, `longitude`, `bike_stands`, `banking`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"

  cursor.execute(sql, vals)

dbEngine.commit()
dbEngine.close()

print("Complete")
