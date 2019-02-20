import datetime
import json
import requests
import boto3
import pymysql.cursors

def stations_to_db(bike_stations):
  for station in bike_stations:
    vals = (station.get('address'), station.get('contract_name'), \
      station.get('name'), station.get('last_update'), station.get('lng'), \
        station.get('lat'), station.get('status'), station.get('available_bikes'), \
          station.get('bonus'), station.get('available_bike_stands'),\
            station.get('number'), station.get('bike_stands'), station.get('banking'))
  return vals

# Allows for timestamping - use as file name for ease of sorting
ts = str(datetime.datetime.now()).split('.')[0].replace(" ", "")

api_key= "9cc2d222a1a4c269a200b0e146162e815f266332"
api_endpoint = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api_key

# retrieve bike stations from JCDecaux API - returns as text file so convert to JSON
r = requests.get(url=api_endpoint)
bike_stations = r.json()

# store bike staions to file locally
path='/home/ubuntu/cycle-psychic/scrape/test/'
file_name=ts+'.json'
with open(path+file_name, 'w') as outfile:
    json.dump(bike_stations, outfile)

# store bike stations to S3
s3_resource = boto3.resource('s3') 
s3_resource.Object('cycle-psychic', file_name).upload_file(Filename=path+file_name)

# store bike stations to RDS - yet to be done

connection = pymysql.connect(
  host='cyclepsychictest.c0mcnyge7xlx.us-east-1.rds.amazonaws.com',
  user='cyclepsychictest',
  password='cyclepsychictest',
  db='cyclepsychictest',
  charset='utf8mb4',
  cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:

        sql = "INSERT INTO all_station_info (name) VALUES (check)"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

connection.close()

# Endpoint: cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com
# Port: 3306
# User: cyclepsychic
# Password: CyclePsychic123