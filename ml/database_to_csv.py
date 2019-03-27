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

query = "SELECT * FROM cyclepsychic.all_station_info;"

cursor.execute(query)
result=cursor.fetchall()
results = csv.writer(open("results_to_23_03_19.csv", "w"))

for row in result:
  results.writerow(row)

connection.close()
