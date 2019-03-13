from flask import render_template
from app import app
import jsonify
import mysql.connector

# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
    )

# prepare to execute statements
cursor = dbEngine.cursor()

@app.route('/')
def index():
  returnDict = {}
  returnDict['user'] = 'Cycle Psychic'
  returnDict['title'] = 'Home'
  return render_template("index.html", **returnDict)

@app.route('/dropdown')
def getStationInfo():
  stations_info = []
  rows = cursor.execute("SELECT * from station_information;")
  for row in rows:
    stations.append(dict(row))
    return jsonify(stations=stations_info)

print(stations_info)
