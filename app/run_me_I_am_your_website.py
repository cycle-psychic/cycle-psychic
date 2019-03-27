from flask import Flask,render_template,jsonify
import requests
import mysql.connector
# import pickle to load in the machine learning model
# import pickle
# from sklearn.linear_model import ElasticNetCV
# from sklearn.preprocessing import StandardScaler
# import math
import datetime

app = Flask(__name__)

# # Load the model and the scaler for predictions
# model = pickle.load(open('model.sav', 'rb'))
# scaler = pickle.load(open('scaler.sav', 'rb'))

# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
)

# prepare to execute statements
cursor = dbEngine.cursor()

#OpenWeather API key
api_key= "cb4ffd84a250fbcb399c9c29cca40597"

# URL to call the API using the ID for Dublin Ciy: 7778677
api_endpoint = "http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=" + api_key + "&units=metric"

@app.route("/")
def root():
    return render_template('index.html')

@app.route('/dropdown')
def getStationInfo():
    stations_info = {}
    cursor.execute("SELECT * from station_information;")
    rows=cursor.fetchall()
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
    currentWeather["Temperature"] = round(data["main"]["temp"]) # round to the nearest INT
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
    locationQuery =  locationSelect+locationVariable

    # execute our query
    cursor.execute(locationQuery)

    # send the result to our dictionary
    locationResult = cursor.fetchall()
    for i in locationResult:
        locationReturn["lat"] = i[0]
        locationReturn["lng"] = i[1]

    return jsonify(locationReturn)

# @app.route('/predict/<station_id>/<time_date>')
# def predict(station_id, time_date):
#     # Assume data and time will come in as ISO 8601 standard
#     # Example: futureDate = (new Date()).toJSON() - "2019-03-23T21:10:58.831Z"
#     # Use the selected station and selected date and time to get prediction
#     date_time_obj = datetime.datetime.strptime('2019-01-04T16:41:24+0200', "%Y-%m-%dT%H:%M:%S%z")
#     weekday = date_time_obj.weekday()
#     hour = date_time_obj.hour
#     minute = date_time_obj.minute
#     features = [[int(station_id), weekday, hour, minute]]
#     scaled_predict = scaler.transform(features)
#     prediction = model.predict(scaled_predict)
#     print("PREDICTION:", prediction)
#     return jsonify({"prediction": math.floor(prediction[0])})

if __name__ == "__main__":
    app.run(debug=True)
