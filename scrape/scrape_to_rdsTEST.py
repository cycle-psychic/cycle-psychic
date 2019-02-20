
import datetime
import json
import requests
import boto3
import pymysql.cursors

# def stations_to_db(bike_stations):
#   for station in bike_stations:
#     vals = (station.get('address'), station.get('contract_name'), \
#       station.get('name'), station.get('last_update'), station.get('lng'), \
#         station.get('lat'), station.get('status'), station.get('available_bikes'), \
#           station.get('bonus'), station.get('available_bike_stands'),\
#             station.get('number'), station.get('bike_stands'), station.get('banking'))
#     return vals

#  sql = "INSERT INTO `all_station_info` (`address`, `contract_name`, `name`, `last_update`, `lng`, `lat`,`status`, `available_bikes`, `bonus`, `available_bike_stands`, `number`, `bike_stands`, `banking`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", vals


ts = str(datetime.datetime.now()).split('.')[0].replace(" ", "")
print("Starting scrape: " + ts)
# retrieve bike stations
api_key= "9cc2d222a1a4c269a200b0e146162e815f266332"
api_endpoint = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api_key
r = requests.get(url=api_endpoint)
bike_stations = r.json()
print(bike_stations[0])
# store bike staions to file locally
#path='/home/ubuntu/src/dummyapp/data/'
file_name=ts+'.json'
#with open(path+file_name, 'w') as outfile:
#    json.dump(bike_stations, outfile)
# store bike stations to S3
#s3_resource = boto3.resource('s3') 
@@@  

#s3_resource.Object('cycle-psychic', file_name).upload_file(Filename=path+file_name)

# store bike stations to RDS
connection = pymysql.connect(
  host='cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com',
  user='cyclepsychic',
  password='CyclePsychic123',
  db='cyclepsychic',
  autocommit=True)

with connection.cursor() as cursor:
  for station in bike_stations:
    vals = (station.get('address'), station.get('contract_name'), \
      station.get('name'), station.get('last_update'), station.get('lng'), \
        station.get('lat'), station.get('status'), station.get('available_bikes'), \
          station.get('bonus'), station.get('available_bike_stands'),\
            station.get('number'), station.get('bike_stands'), station.get('banking'))
    sql = "INSERT INTO `all_station_info` (`address`, `contract_name`, `name`, `last_update`, `lng`, `lat`,`status`, `available_bikes`, `bonus`, `available_bike_stands`, `number`, `bike_stands`, `banking`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql, vals)
  result = cursor.fetchone()
  print(result)

connection.close()