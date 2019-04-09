#Import pandas and scikitlearn for Machine Learning Models
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesRegressor

# Pickle saves the model
import pickle

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

df = pd.read_csv('./bike+weather_to_28_03_19.csv')


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

  estimator = ExtraTreesRegressor()
  estimator.fit(scaled_train_features, train_targets)

  return scaler, estimator


# Cycle through station numbers 2 to 115
for station in range (2,116):
  if station != 20:  
    print('Training station: ' , str(station))
    df = pd.read_csv('./bike+weather_to_28_03_19.csv')
    df = df.loc[df['number'] == station]
    scaler, estimator = train_station(df)
    print('Saving model and scaler for station: ' , str(station))
    filename_est = '../app/models/model'+str(station)+'.sav'
    filename_scaler = '../app/models/scaler'+str(station)+'.sav'
    pickle.dump(estimator, open(filename_est, 'wb'))
    pickle.dump(scaler, open(filename_scaler, 'wb'))