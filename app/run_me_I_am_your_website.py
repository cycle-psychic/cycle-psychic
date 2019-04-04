from flask import Flask, render_template, jsonify
import requests
import mysql.connector

import datetime

app = Flask(__name__)

# # # Load the model and the scaler for predictions
# # model = pickle.load(open('model.sav', 'rb'))
# # scaler = pickle.load(open('scaler.sav', 'rb'))
#
# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
)

# prepare to execute statements
cursor = dbEngine.cursor()

# OpenWeather API key
api_key = "cb4ffd84a250fbcb399c9c29cca40597"

# URL to call the API using the ID for Dublin Ciy: 7778677
api_endpoint = "http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=" + api_key + "&units=metric"


@app.route("/")
def root():
    return render_template('index.html')


@app.route('/dropdown')
def getStationInfo():
    stations_info = {}
    cursor.execute("SELECT * from station_information;")
    rows = cursor.fetchall()
    for row in rows:
        # create object of key:value pairs
        this_station = {}

        # define the value for each key value pair and send it to the dictionary
        station_id = row[0]
        this_station["ID"] = row[0]
        this_station["City"] = row[1]
        this_station["Name"] = row[2]
        this_station["Address"] = row[3]
        this_station["Latitude"] = row[4]
        this_station["Longitude"] = row[5]
        stations_info[station_id] = this_station

    return jsonify(stations_info)


@app.route("/weather")
def getWeather():
    # retrieve weather information from OpenWeather API - returns as text file so convert to JSON
    r = requests.get(url=api_endpoint)
    data = r.json()

    # initialise empty dict to store weather data
    currentWeather = {}

    # get the data we want out of the response
    currentWeather["Temperature"] = round(data["main"]["temp"])  # round to the nearest INT
    currentWeather["High"] = round(data["main"]["temp_max"])
    currentWeather["Low"] = round(data["main"]["temp_min"])
    currentWeather["Wind"] = data["wind"]["speed"]
    currentWeather["Description"] = data["weather"][0]["description"]
    currentWeather["Summary"] = data["weather"][0]["main"]
    currentWeather["iconURL"] = "http://openweathermap.org/img/w/" + data["weather"][0]["icon"] + ".png"

    return jsonify(currentWeather)


@app.route('/getlocation/<station_id>')
def getStationLocation(station_id):
    # store the data to send back to front end
    locationReturn = {}

    # define our query
    locationSelect = "SELECT latitude, longitude FROM station_information WHERE station_number = "
    locationVariable = str(station_id)
    locationQuery = locationSelect + locationVariable

    # execute our query
    cursor.execute(locationQuery)

    # send the result to our dictionary
    locationResult = cursor.fetchall()
    for i in locationResult:
        locationReturn["lat"] = i[0]
        locationReturn["lng"] = i[1]

    return jsonify(locationReturn)

@app.route('/avgchart/<station_address>')
def avgChartData(station_address):
    # get current date
    date = datetime.datetime.now()
    day = date.strftime("%A")

    station_address = station_address
    station_address = station_address.replace("_"," ")
    print(station_address)

    # Holds average bikes organised by hour
    averageByHour = {}

    # command to code below
    cursor.execute("SELECT AVG(available_bikes),last_update FROM all_station_info WHERE WEEKDAY(last_update)=\""+day+"\" AND address=\""+station_address+"\" GROUP BY hour(last_update);")
    rows = cursor.fetchall()

    for row in rows:
        hour = row[1].strftime("%H")
        averageByHour[hour] = int(round(row[0]))

    return jsonify(averageByHour)

if __name__ == "__main__":
    app.run(debug=True)
