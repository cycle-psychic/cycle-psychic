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

@app.route('/predict/<station_id>/<time_date>')
def predict(station_id, time_date):
    # Assume data and time will come in as ISO 8601 standard
    # Example: futureDate = (new Date()).toJSON() - "2019-03-23T21:10:58.831Z"
    # Use the selected station and selected date and time to get prediction
    date_time_obj = datetime.datetime.strptime(time_date, "%Y-%m-%dT%H:%M:%S.%fZ") # changed %z to .%fZ
    weekday = date_time_obj.weekday()
    hour = date_time_obj.hour
    minute = date_time_obj.minute
    features = [[int(station_id), weekday, hour, minute]]
    scaled_predict = scaler.transform(features)
    prediction = model.predict(scaled_predict)
    print("PREDICTION:", prediction)
   # return jsonify({"prediction": math.floor(prediction[0])})
    return math.floor(prediction[0])

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
