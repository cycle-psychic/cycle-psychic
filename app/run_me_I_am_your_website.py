from flask import Flask,render_template,jsonify
import mysql.connector

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

if __name__ == "__main__":
    app.run(debug=True)
