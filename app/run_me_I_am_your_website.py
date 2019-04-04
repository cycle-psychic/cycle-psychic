from flask import Flask,render_template,jsonify
import mysql.connector
# import pickle to load in the machine learning model
import pickle
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
import math
import datetime

app = Flask(__name__)

# Load the model and the scaler for predictions
model = pickle.load(open('model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# build engine for databasee
dbEngine = mysql.connector.connect(
    host="cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com",
    user="cyclepsychic",
    passwd="CyclePsychic123",
    database="cyclepsychic",
)

# prepare to execute statements
cursor = dbEngine.cursor()

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/test")
def test():
    return render_template('test.html')

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

def predict(station_id, time_date):
    # Required fields: number, hour, minute, main_temp, main_wind_speed,
    # main_rain_volume_1h, main_snow_volume_1h, Monday, Tuesday,
    # Wednesday, Thursday, Friday, Saturday, Sunday, clouds(800 -899),
    # atmosphere (700-799), snow(600-699), light_rain(500), rain(501-599), light_drizzle(300),
    # drizzle (301 - 399), thunderstorm (200 - 299)
    
    # Assume data and time will come in as ISO 8601 standard
    # Example: futureDate = (new Date()).toJSON() - "2019-03-23T21:10:58.831Z"
    # Use the selected station and selected date and time to get prediction
    date_time_obj = datetime.datetime.strptime('2019-01-04T16:41:24+0200', "%Y-%m-%dT%H:%M:%S%z")
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
    print("PREDICTION:", prediction)
    return jsonify({"prediction": math.floor(prediction[0])})

if __name__ == "__main__":
    app.run(debug=True)
