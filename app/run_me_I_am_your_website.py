from flask import Flask, render_template, jsonify
import requests
import mysql.connector

import datetime
import math

app = Flask(__name__)


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

def predict(station_id, time_date, weather_id, main_temp, main_wind_speed, main_rain_volume_1h, main_snow_volume_1h):
    '''
    Function calls the models and scalers for the relevant station.
    The predicts the number of bikes available for that station. 
    '''
    # Load the model and the scaler for predictions
    with open('./models/model'+str(station_id)+'.sav', 'rb') as file1:
        model = pickle.load(file1)

    with open('./models/scaler'+str(station_id)+'.sav', 'rb') as file2:
        scaler = pickle.load(file2)

    # Break apart time and date into weekday, hour and minute
    date_time_obj = datetime.datetime.strptime(time_date, "%Y-%m-%dT%H:%M:%S.%fZ") # changed %z to .%fZ
    weekday = date_time_obj.weekday()
    hour = date_time_obj.hour
    minute = date_time_obj.minute

    Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday = 0,0,0,0,0,0,0
    clouds, atmosphere, snow, light_rain, rain, light_drizzle, drizzle, thunderstorm = 0,0,0,0,0,0,0,0
    
    # Set day of the week
    if weekday == 0:
        Monday = 1
    elif weekday == 1:
        Tuesday = 1
    elif weekday == 2:
        Wednesday = 1
    elif weekday == 3:
        Thursday = 1
    elif weekday == 4:
        Friday = 1
    elif weekday == 5:
        Saturday = 1
    elif weekday == 6:
        Sunday = 1

    # Set weather based on weather id. 
    if 200 <= weather_id < 300:
        thunderstorm = 1
    elif weather_id == 300:
        light_drizzle = 1
    elif 300 <= weather_id < 400:
        drizzle = 1
    elif weather_id == 500:
        light_rain = 1
    elif 500 <= weather_id < 600:
        rain = 1
    elif 600 <= weather_id < 700:
        snow = 1
    elif 700 <= weather_id < 800:
        atmosphere = 1
    elif 800 <= weather_id < 900:
        clouds = 1

    # Set the features and pass into scaler and model
    features = [[int(station_id), hour, minute,main_temp, main_wind_speed,
    main_rain_volume_1h, main_snow_volume_1h, Monday, Tuesday,
    Wednesday, Thursday, Friday, Saturday, Sunday, clouds,
    atmosphere, snow, light_rain, rain, light_drizzle,
    drizzle, thunderstorm]]

    scaled_predict = scaler.transform(features)
    prediction = model.predict(scaled_predict)
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
    cursor.execute("select distinct s.station_number, s.address, s.latitude, s.longitude, a.bike_stands, a.banking \
    from station_information s, all_station_info a \
    where s.station_number = a.number;")
    rows=cursor.fetchall()
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
