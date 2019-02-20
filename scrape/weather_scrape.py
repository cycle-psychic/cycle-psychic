import datetime
import json
import requests
import boto3

# Allows for timestamping - use as file name for ease of sorting
ts = str(datetime.datetime.now()).split('.')[0].replace(" ", "")

#enter your key for the OpenWeather API below
api_key= "enteryourkeyhere"

#call the API using the ID for Dublin Ciy: 7778677 
api_endpoint = "http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=" + api_key

# retrieve weather information from OpenWeather API - returns as text file so convert to JSON
r = requests.get(url=api_endpoint)
weather_info = r.json()

# store weather info to file locally
path = '/home/ubuntu/cycle-psychic/scrape/weather/'
file_name = 'data'+ts+'.json'
with open(path+file_name, 'w') as outfile:
    json.dump(weather_info, outfile)

# store weather info to S3
s3_resource = boto3.resource('s3')
s3_resource.Object('cycle-psychic-weather', file_name).upload_file(Filename=path+file_name)

# store weather info to RDS - yet to be done
