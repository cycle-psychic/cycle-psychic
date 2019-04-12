import mysql.connector
import csv
import pandas as pd
import numpy as np
import datetime
import math
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
import pickle
import time
import os

def save_to_csv():
  '''
  Function to save information from database to csv
  '''
  # Connect to database
  connection = mysql.connector.connect(
    host='cyclepsychic.c7jha7i6ueuc.eu-west-1.rds.amazonaws.com',
    user='cyclepsychic',
    password='CyclePsychic123',
    db='cyclepsychic')

  cursor = connection.cursor()

  # Create query to select all rows from station info
  query = "SELECT * FROM cyclepsychic.all_station_info;"

  cursor.execute(query)
  result=cursor.fetchall()
  # Change this to date created
  results = csv.writer(open("results_bikes.csv", "w"))

  # Write each row into the csv file
  for row in result:
    results.writerow(row)

  # Create a query to select all weather from the database
  query = "SELECT * FROM cyclepsychic.city_weather;"

  cursor.execute(query)
  result=cursor.fetchall()
  # Change this to date created
  results = csv.writer(open("results_weather.csv", "w"))

  for row in result:
    results.writerow(row)

  connection.close()

def clean_and_merge_data():
  # Read in bike and weather data. Convert last_update to a datetime format
  df = pd.read_csv('results_bikes.csv', names=['address', 'contract_name', 'name', 'last_update', 'lng', 'lat', 'status', 'available_bikes', 'bonus', 'available_bike_stands', 'number', 'bike_stands', 'banking'])
  df['last_update'] = pd.to_datetime(df['last_update'])
  df_weather = pd.read_csv('results_weather.csv', names=['city_id', 'last_update', 'city_name', 'longitude', 'latitude', 'weather_id', 'weather_description', 'weather_main', 'main_temp', 'main_pressure', 'main_humidity', 'main_temp_min', 'main_temp_max', 'main_sea_level', 'main_wind_speed', 'main_wind_direction', 'main_clouds', 'main_rain_volume_1h', 'main_rain_volume_3h', 'main_snow_volume_1h', 'main_snow_volume_3h', 'base', 'main_grnd_level', 'sys_id', 'sys_type', 'sys_message', 'sys_country', 'sys_sunrise', 'sys_sunset', 'cod', 'weather_icon'])
  df_weather['last_update'] = pd.to_datetime(df_weather['last_update'])

  # Drop bike data where there is no corresponding weather data
  df = df[(df['last_update'] > '2019-02-17 12:00:00')]

  # Convert date to a day of the week in a new column. 
  # Create new column with hour
  # Create new column with minute
  # Do for both bikes and weather

  df['weekday'] = df['last_update']
  df['hour'] = df['last_update']
  df['minute'] = df['last_update']
  df['date'] = df['last_update']

  df['weekday'] = df['weekday'].apply(lambda date: datetime.datetime.weekday(date))
  df['hour'] = df['hour'].apply(lambda time: time.hour)
  df['minute'] = df['minute'].apply(lambda time: math.floor(time.minute/5) * 5)
  df['date'] = df['date'].apply(lambda date: str(date.day)+str(date.month)+str(date.year))

  df_weather['weekday'] = df_weather['last_update']
  df_weather['hour'] = df_weather['last_update']
  df_weather['minute'] = df_weather['last_update']
  df_weather['date'] = df_weather['last_update']

  df_weather['weekday'] = df_weather['weekday'].apply(lambda date: datetime.datetime.weekday(date))
  df_weather['hour'] = df_weather['hour'].apply(lambda time: time.hour)
  df_weather['minute'] = df_weather['minute'].apply(lambda time: math.floor(time.minute/5) * 5)
  df_weather['date'] = df_weather['date'].apply(lambda date: str(date.day)+str(date.month)+str(date.year))

  # Join the two tables on the date and time
  df = pd.merge(df, df_weather,how = 'outer', on=['date', 'hour', 'minute', 'weekday'])
  df = df.sort_values(by=['last_update_x', 'last_update_y'])

  # Drop row where weather information has come in with no corresponding bike data
  index = np.where(df['address'].isna())
  df.drop(df.index[[index]], inplace = True)

  # Drop all rows where the value is closed
  df = df[df.status != 'CLOSED']

  # Drop bank holiday - not representative of usage
  df = df[df.date != '1832019']

  # Update the hour by 1 after March 31 to account for daylight savings
  df['hour'] = np.where(df['last_update_x'] >= '2019-03-31 01:00', df['hour']+ 1, df['hour'])
  df['hour'] = np.where(df['hour'] == 24, 0, df['hour'])

  # Drop unneeded columns
  df.drop(['name', 'address', 'contract_name', 'lng', 'lat', 
         'available_bike_stands', 'last_update_x', 'last_update_y',
         'banking', 'city_id', 'city_name', 'longitude',
        'latitude', 'main_pressure', 'main_humidity', 'main_temp_min',
        'main_temp_max', 'main_sea_level', 'main_wind_direction',
        'main_clouds', 'main_rain_volume_3h', 'main_snow_volume_3h',
        'base', 'main_grnd_level', 'sys_id', 'sys_type',
        'sys_message', 'sys_message', 'sys_sunrise', 'sys_sunset',
        'cod', 'weather_icon', 'sys_country', 'bonus', 'date', 'status', 
        'bike_stands', 'weather_description', 'weather_main'], axis=1, inplace = True)

  # Forward fill any rows with missing weatehr data
  df = df.fillna(method='ffill')

  # Seperate out weekdays into seperate columns with 1 or 0 value
  # Avoid applying weighted importance to days
  df['Monday'] = np.where(df['weekday'] == 0, 1,0)
  df['Tuesday'] = np.where(df['weekday'] == 1, 1,0)
  df['Wednesday'] = np.where(df['weekday'] == 2, 1,0)
  df['Thursday'] = np.where(df['weekday'] == 3, 1,0)
  df['Friday'] = np.where(df['weekday'] == 4, 1,0)
  df['Saturday'] = np.where(df['weekday'] == 5, 1,0)
  df['Sunday'] = np.where(df['weekday'] == 6, 1,0)

  # Seperate out the weather ids also. 
  # Avoid weighting the ids - get description from db
  df['clouds'] = np.where((df['weather_id'] < 900) & (df['weather_id'] >= 800) , 1,0)
  df['atmosphere'] = np.where((df['weather_id'] < 800) & (df['weather_id'] >= 700) , 1,0)
  df['snow'] = np.where((df['weather_id'] < 700) & (df['weather_id'] >= 600) , 1,0)
  df['light_rain'] = np.where(df['weather_id'] == 500, 1,0)
  df['rain'] = np.where((df['weather_id'] < 600) & (df['weather_id'] >= 501), 1,0)
  df['light_drizzle'] = np.where(df['weather_id'] == 300, 1,0)
  df['drizzle'] = np.where((df['weather_id'] < 400) & (df['weather_id'] >= 301), 1,0)
  df['thunderstorm'] = np.where((df['weather_id'] < 300) & (df['weather_id'] >= 200), 1,0)

  # Can drop weekday and weather_id 
  df.drop(['weekday', 'weather_id'], axis = 1, inplace = True)

  # Save to new csv file
  df.to_csv('bike_weather_data.csv')

def split_by_position(features, targets):
    """
    train 0.80
    test 0.20
    """
    len_train = int(0.80 * len(features))
    train_features = features[0:len_train]
    train_targets = targets[0:len_train]
    test_features = features[len_train:]
    test_targets = targets[len_train:]
    return train_features, test_features, train_targets, test_targets

def train_station(station_df):
  features = station_df[['number', 'hour', 'minute',
              'main_temp', 'main_wind_speed', 'main_rain_volume_1h', 'main_snow_volume_1h',
              'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
              'Sunday', 'clouds', 'atmosphere', 'snow', 'light_rain',
              'rain', 'light_drizzle', 'drizzle', 'thunderstorm']].values
  targets = station_df['available_bikes'].values

  train_features, test_features, train_targets, test_targets = split_by_position(features, targets)

  scaler = StandardScaler()
  scaler.fit(train_features)
  scaled_train_features = scaler.transform(train_features)

  estimator = GradientBoostingRegressor()
  estimator.fit(scaled_train_features, train_targets)

  return scaler, estimator

#then = time.time()
save_to_csv()
clean_and_merge_data()
for station in range (2,116):
  if station != 20:  
    print('Training station: ' , str(station))
    df = pd.read_csv('./bike_weather_data.csv')
    df = df.loc[df['number'] == station]
    scaler, estimator = train_station(df)
    print('Saving model and scaler for station: ' , str(station))
    filename_est = '../app/models/model'+str(station)+'.sav'
    filename_scaler = '../app/models/scaler'+str(station)+'.sav'
    pickle.dump(estimator, open(filename_est, 'wb'))
    pickle.dump(scaler, open(filename_scaler, 'wb'))
#now = time.time()
#print("It took:", now-then, "seconds")