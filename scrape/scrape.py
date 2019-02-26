from datetime import datetime
import json
import requests
import boto3
import mysql.connector

# Allow date and time stamp be file names
ts = str(datetime.now()).split('.')[0].replace(" ", "")
print("Starting scrape: " + ts)

# retrieve bike stations
api_key= "9cc2d222a1a4c269a200b0e146162e815f266332"
api_endpoint = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api_key

r = requests.get(url=api_endpoint)
bike_stations = r.json()

file_name=ts+'.json'

# store bike staions to file locally - change as required
path='/home/ubuntu/cycle-psychic/scrape/data/'
file_name=ts+'.json'
with open(path+file_name, 'w') as outfile:
    json.dump(bike_stations, outfile)

# store bike stations to S3 as backup
# 'cycle-psychic' is the bucket to save to and file_name is the name you want it to have)
s3_resource = boto3.resource('s3') 
s3_resource.Object('cycle-psychic', file_name).upload_file(Filename=path+file_name)

# store bike stations to RDS - open connection with rds details
connection = mysql.connector.connect(
  host='cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com',
  user='cyclepsychic',
  password='CyclePsychic123',
  db='cyclepsychic')

cursor = connection.cursor()

for station in bike_stations:
  vals = (station.get('address'), station.get('contract_name'), \
    station.get('name'), datetime.fromtimestamp(int(station.get('last_update'))/1000), station['position'].get('lng'), \
      station['position'].get('lat'), station.get('status'), station.get('available_bikes'), \
        station.get('bonus'), station.get('available_bike_stands'),\
          station.get('number'), station.get('bike_stands'), station.get('banking'))
  sql = "INSERT IGNORE INTO `all_station_info` (`address`, `contract_name`, `name`, `last_update`, `lng`, `lat`,`status`, `available_bikes`, `bonus`, `available_bike_stands`, `number`, `bike_stands`, `banking`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
  cursor.execute(sql, vals)

connection.commit()
connection.close()
                                             