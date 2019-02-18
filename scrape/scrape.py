import datetime
import json
import requests
import boto3

# Allows for timestamping - use as file name for ease of sorting
ts = str(datetime.datetime.now()).split('.')[0].replace(" ", "")

api_key= "9cc2d222a1a4c269a200b0e146162e815f266332"
api_endpoint = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api_key

# retrieve bike stations from JCDecaux API - returns as text file so convert to JSON
r = requests.get(url=api_endpoint)
bike_stations = r.json()

# store bike staions to file locally
path='/home/ubuntu/cycle-psychic/scrape/data/'
file_name=ts+'.json'
with open(path+file_name, 'w') as outfile:
    json.dump(bike_stations, outfile)

# store bike stations to S3
s3_resource = boto3.resource('s3') 
s3_resource.Object('cycle-psychic', file_name).upload_file(Filename=path+file_name)

# store bike stations to RDS - yet to be done