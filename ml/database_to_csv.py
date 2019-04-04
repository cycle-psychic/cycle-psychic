'''
Script to convert info from the database to a csv
This converts both the weather and the bikes
'''
# Used to convert data from database to csv
import mysql.connector
import csv

# Connect to database
connection = mysql.connector.connect(
  host='cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com',
  user='cyclepsychic',
  password='CyclePsychic123',
  db='cyclepsychic')

cursor = connection.cursor()

# Create query to select all rows from station info
query = "SELECT * FROM cyclepsychic.all_station_info;"

cursor.execute(query)
result=cursor.fetchall()
# Change this to date created
results = csv.writer(open("results_bikes_to_28_03_19.csv", "w"))

# Write each row into the csv file
for row in result:
  results.writerow(row)

# Create a query to select all weather from the database
query = "SELECT * FROM cyclepsychic.city_weather;"

cursor.execute(query)
result=cursor.fetchall()
# Change this to date created
results = csv.writer(open("results_weather_to_28_03_19.csv", "w"))

for row in result:
  results.writerow(row)

connection.close()
