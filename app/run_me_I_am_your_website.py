from flask import Flask, render_template, jsonify
import requests
import mysql.connector
from sklearn.preprocessing import StandardScaler
import pickle
import math
import datetime
from datetime import timedelta

app = Flask(__name__)

# Load the model and the scaler for predictions
model = pickle.load(open('model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))
#
# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
)

cursor = dbEngine.cursor()


def open_connection(query):
    cursor = dbEngine.cursor()
    try:
        # Execute query
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        cursor.close()
    return rows


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
    query = "SELECT * from station_information;"
    rows = open_connection(query)
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

    # get results and send the to our dictionary
    locationResult = open_connection(locationQuery)
    for i in locationResult:
        locationReturn["lat"] = i[0]
        locationReturn["lng"] = i[1]

    return jsonify(locationReturn)


@app.route('/avgchart/<station_address>')
def avgChartData(station_address):
    # build engine for databasee
    dbEngine = mysql.connector.connect(
        host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
        user="cyclepsychic",
        passwd="CyclePsychic123",
        database="cyclepsychic",
    )

    cursor = dbEngine.cursor()

    # get current date
    date = datetime.datetime.now()
    day = date.strftime("%A")

    station_address = station_address
    station_address = station_address.replace("_"," ")

    # Holds average bikes organised by hour
    averageByHour = {}
    cursor.execute("SELECT AVG(available_bikes),last_update FROM all_station_info WHERE WEEKDAY(last_update)=\""+day+"\" AND address=\""+station_address+"\" GROUP BY hour(last_update);")
    rows = cursor.fetchall()
    cursor.close()
    for row in rows:
        hour = row[1].strftime("%H")
        averageByHour[hour] = int(round(row[0]))

    return jsonify(averageByHour)

@app.route('/bikes1week/<station_address>')
def bikes_available_1week(station_address):

    # get current date
    date = datetime.datetime.now()
    # remove trailing minutes (to check for available bikes during this hour)
    date = date.replace(minute=0,second=0,microsecond=0)
    # convert time to hours only
    hour = date.strftime("%X")

    # add 59 minutes and 59 seconds for SQL query and format it correctly
    datePlusOneHour = date + timedelta(hours=1) - timedelta(seconds=1)
    datePlusOneHour = str(datePlusOneHour)
    datePlusOneHour = datePlusOneHour.split(" ")[1]

    # fix the URL request for a specific station
    station_address = station_address
    station_address = station_address.replace("_"," ")

    # build query
    static_query1 = """ SELECT avg(available_bikes), last_update as Weekday
                FROM all_station_info 
                WHERE cast(last_update as time) between \'"""
    static_query2 = hour + "\' and \'" + str(datePlusOneHour)
    static_query3 = "\' AND address=\'" + station_address
    static_query4 = "\' AND YEARWEEK(last_update) = yearweek(NOW() - INTERVAL 1 WEEK) Group by Weekday(last_update);"
    constructedQuery = static_query1 + static_query2 + static_query3 + static_query4

    # Holds average bikes organised by hour
    daily_available_bikes = {}

    # execute
    rows = open_connection(constructedQuery)

    for row in rows:
        weekday =  row[1].strftime('%a')
        daily_available_bikes[weekday] = round(row[0])

    return jsonify(daily_available_bikes)

def predict(station_id, time_date):
    # Required fields: number, hour, minute, main_temp, main_wind_speed,
    # main_rain_volume_1h, main_snow_volume_1h, Monday, Tuesday,
    # Wednesday, Thursday, Friday, Saturday, Sunday, clouds(800 -899),
    # atmosphere (700-799), snow(600-699), light_rain(500), rain(501-599), light_drizzle(300),
    # drizzle (301 - 399), thunderstorm (200 - 299)
    
    # Assume data and time will come in as ISO 8601 standard
    # Example: futureDate = (new Date()).toJSON() - "2019-03-23T21:10:58.831Z"
    # Use the selected station and selected date and time to get prediction
    date_time_obj = datetime.datetime.strptime(time_date, "%Y-%m-%dT%H:%M:%S.%fZ") # changed %z to .%fZ
    weekday = date_time_obj.weekday()
    hour = date_time_obj.hour
    minute = date_time_obj.minute
    Monday = 1
    Tuesday = 0
    Wednesday = 0
    Thursday = 0
    Friday = 0
    Saturday = 0
    Sunday = 0
    main_temp = 0
    main_wind_speed = 0
    main_rain_volume_1h = 0
    main_snow_volume_1h = 0
    clouds = 1
    atmosphere = 0
    snow = 0
    light_rain = 0
    rain = 0
    light_drizzle = 0
    drizzle = 0
    thunderstorm = 0
    features = [[int(station_id), hour, minute,main_temp, main_wind_speed,
    main_rain_volume_1h, main_snow_volume_1h, Monday, Tuesday,
    Wednesday, Thursday, Friday, Saturday, Sunday, clouds,
    atmosphere, snow, light_rain, rain, light_drizzle,
    drizzle, thunderstorm]]
    scaled_predict = scaler.transform(features)
    prediction = model.predict(scaled_predict)
   # return jsonify({"prediction": math.floor(prediction[0])})
    return math.floor(prediction)

@app.route('/predictall/<datetime>')
def predictall(datetime):
    """This function takes a datetime object as input (should be in ISO 8601 standard format).
    The function then calls the database to get some station information: ID, latitude, longitude, stands, card payments.
    It then loops through all stations and requests a prediction using the predict() function.
    Station information is then almagated with the prediction and returned as a JSON object.
    """
    # declare a dictionary to store station data
    data = {}
    # call the database to get the static information
    query = "select distinct s.station_number, s.address, s.latitude, s.longitude, a.bike_stands, a.banking \
    from station_information s, all_station_info a \
    where s.station_number = a.number;"
    rows=open_connection(query)
    # loop through each row returned
    for row in rows:
        # create a dictionary for the station
        station = {}
        # add static data to the dictionary
        station["id"] = row[0]
        station["address"] = row[1]
        station["lat"] = row[2]
        station["lng"] = row[3]
        station["bike_stands"] = row[4]
        # check value of "banking" and assign it a true or false value
        if row[5] == '1':
            station["banking"] = "true"
        else:
            station["banking"] = "false"

        # call predict() to get the prediction for this station
        prediction = predict(row[0], datetime)

        # add predicted bike number to the dictionary
        station["available_bikes"] = prediction
        # subtract bike prediction from total stands at station to get stand prediction
        station["available_bike_stands"] = row[4] - prediction

        # add the current station dictionary to the data list
        data[row[0]] = station

    # return the data as a JSON object
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
