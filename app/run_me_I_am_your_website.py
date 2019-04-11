from flask import Flask, render_template, jsonify
import requests
import mysql.connector
import pickle
import datetime
import math
from datetime import timedelta

app = Flask(__name__)

# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
)

cursor = dbEngine.cursor()

# this function opens a database query for a connection
def open_connection(query):
    cursor = dbEngine.cursor()
    try:
        # Execute query
        cursor.execute(query)
        rows = cursor.fetchall()
    except TypeError(e):
        print(e)
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
    """ This function populates the dropdown menu based on the database query. It doesn't expect any inputs. """

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
    """ This function gets up to date weather information from the openweather api. No inputs are required. """
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
    """ This function retrives a given station's longitude and latitude from
        the database and returns it as a JSON object. """
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
    """ This function queries the database to get up to date information about the average bike availability for the
        current hour. It expects the station address to be provided and outputs an average by hour for the current day
        based on historical average. """
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
    """ This function gets the historical data for the number of bikes available on a given day at the current timeslot.
        It expects the station address as the input and provides the number of available bikes at the current hour
        based on the previous Week's data (indexed by day name). """

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
    cursor.execute(constructedQuery)
    rows = cursor.fetchall()
    for row in rows:
        weekday =  row[1].strftime('%a')
        daily_available_bikes[weekday] = round(row[0])
    cursor.close()
    return jsonify(daily_available_bikes)

@app.route('/bikes2weeks/<station_address>')
def bikes_available_2weeks(station_address):
    """ This function retrives the bike availability for the previous 14 days at the current hour. It expects the station
        address as its input and returns the number of bikes available indexed by the date. """
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
    static_query1 = """ SELECT avg(available_bikes), last_update
                FROM all_station_info 
                WHERE cast(last_update as time) between \'"""
    static_query2 = hour + "\' and \'" + str(datePlusOneHour)
    static_query3 = "\' AND address=\'" + station_address
    static_query4 = "\' AND last_update >= now() - INTERVAL 14 DAY Group by CAST(last_update AS DATE);"
    constructedQuery = static_query1 + static_query2 + static_query3 + static_query4

    # Holds average bikes organised by hour
    daily_available_bikes = {}

    # execute
    cursor.execute(constructedQuery)
    rows = cursor.fetchall()
    for row in rows:
        weekday =  row[1].strftime('%x')
        daily_available_bikes[weekday] = round(row[0])
    cursor.close()
    return jsonify(daily_available_bikes)

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

def weather_forecast():
    """This function calls the Openweather API to get a weather forecast. 
    Data is returned as a JSON file."""

    #call the API using the ID for Dublin City: 7778677 
    api_endpoint = "http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=" + api_key

    # retrieve weather information from OpenWeather API - returns as text file so convert to JSON
    r = requests.get(url=api_endpoint)
    data = r.json()

    # return the data
    return data

@app.route('/predictall/<time_date>')
def predictall(time_date):
    """This function takes a datetime object as input (should be in ISO 8601 standard format).
    The function calls the Openweather Forecast API to find weather forecast info for the relevant time.
    The function then calls the database to get some station information: ID, latitude, longitude, stands, card payments.
    It then loops through all stations and requests a prediction using the predict() function.
    Station information is then almagated with the prediction and returned as a JSON object.
    """
    # convert the input to a datetime object
    date_time_obj = datetime.datetime.strptime(time_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # call the weather forecast API
    weather_data = weather_forecast()

    # intialise variable to check whether relevant weather data has been found in the JSON file
    found = False

    # loop through the weather data to find the closest time/date to the prediction time/date
    for item in weather_data["list"]:
        # for each item, get the date and convert
        dt = item.get("dt")
        timestamp = datetime.datetime.utcfromtimestamp(dt)

        # get the time difference between the input and the date in the file
        time_diff = timestamp - date_time_obj
        time_diff_hours = time_diff.total_seconds()/3600    # get time_diff in hours
        
        # if the time difference is less than 3, then use this list item for the weather forecast
        if (0 <= time_diff_hours <= 3):
            # update found to True
            found = True

            # extract weather data from the JSON
            weather_id = item.get("weather")[0].get("id")
            print("Weather Id:", weather_id)
            temp = item.get("main").get("temp")
            print("Temp:", temp)
            if "wind" in item:
                wind_speed = item.get("wind").get("speed")
            else:
                wind_speed = 0
            print("Wind Speed:", wind_speed)
            if "rain" in item and "3h" in item["rain"]:
                    rain_volume = item.get("rain").get("3h")
            else:
                rain_volume = 0
            print("Rain Volume:", rain_volume)
            if "snow" in item and "3h" in item["snow"]:
                snow_volume = item.get("snow").get("3h")
            else:
                snow_volume = 0
            print("Snow Volume:", snow_volume)

            # once weather is found, break out of the loop
            break

    # after each item has been checked, if relevant data has not been found, assign some default values
    if (not found):
        print("Weather Forecast not available. Using default values for Prediction.")
        weather_id = 800
        temp = 283
        wind_speed = 7.5
        rain_volume = 0
        snow_volume = 0
    
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
        prediction = predict(row[0], time_date, weather_id, temp, wind_speed, rain_volume, snow_volume)

        # add predicted bike number to the dictionary
        station["available_bikes"] = prediction
        # subtract bike prediction from total stands at station to get stand prediction
        station["available_bike_stands"] = row[4] - prediction

        # add the current station dictionary to the data list
        data[row[0]] = station

    # return the data as a JSON object
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
