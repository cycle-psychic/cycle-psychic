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

query = "SELECT * FROM cyclepsychic.all_station_info WHERE last_update BETWEEN '2019-03-05' and '2019-03-13';"

cursor.execute(query)
result=cursor.fetchall()
week_of_results = csv.writer(open("05-13-03-19_results.csv", "w"))

for row in result:
  week_of_results.writerow(row)

connection.close()
