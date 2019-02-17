import datetime
import json
import requests

# Allows for timestamping - use as file name for ease of sorting
ts = str(datetime.datetime.now()).split('.')[0].replace(" ", "")

api_key= "92ce20215ef36bf9620e984c17f0881f"

#call the API using the ID for Dublin Ciy: 7778677 
api_endpoint = "http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=" + api_key

# retrieve weather information from OpenWeather API - returns as text file so convert to JSON
r = requests.get(url=api_endpoint)
weather_info = r.json()

# store weather info to file locally
with open('/home/ubuntu/cycle-psychic/scrape/weather/data' + ts + '.json', 'w') as outfile:
    json.dump(weather_info, outfile)

# store weather info to S3 - yet to be done

# store weather info to RDS - yet to be done