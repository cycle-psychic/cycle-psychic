import datetime
import json
import requests

# Allows for timestamping - use as file name for ease of sorting
ts = str(datetime.datetime.now()).split('.')[0].replace(" ", "")

api_key= "9cc2d222a1a4c269a200b0e146162e815f266332"
api_endpoint = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + api_key

# retrieve bike stations from JCDecaux API - returns as text file so convert to JSON
r = requests.get(url=api_endpoint)
bike_stations = r.json()

# store bike staions to file locally
with open('/home/ubuntu/cycle-psychic/scrape/data' + ts + '.json', 'w') as outfile:
    json.dump(bike_stations, outfile)

# store bike stations to S3 - yet to be done

# store bike stations to RDS - yet to be done