import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import os

temp_df = pd.read_csv('temperature.csv')
hum_df = pd.read_csv('humidity.csv')
pres_df = pd.read_csv('pressure.csv')

# FIx the null values
print(f"Null values in the temperature dataset: {temp_df.isna().sum()}")
print(f"Null values in the humidity dataset: {hum_df.isna().sum()}")
print(f"Null values in the pressure dataset: {pres_df.isna().sum()}")

# Remove all the rows with null values
temp_df = temp_df.dropna()
hum_df = hum_df.dropna()
pres_df = pres_df.dropna()

# Check again if all the null values are removed
print(f"Null values in the temperature temperature after cleaning: {temp_df.isna().sum()}")
print(f"Null values in the temperature humidity after cleaning: {hum_df.isna().sum()}")
print(f"Null values in the temperature pressure after cleaning: {pres_df.isna().sum()}")


def prepare_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    X, y = [], []
    for i in range(len(scaled_data) - 11):
        X.append(scaled_data[i:i+10, 0])
        y.append(scaled_data[i+10, 0])
    return np.array(X), np.array(y), scaler

# Load datasets
temp_data = temp_df['Temperature'].values
hum_data = hum_df['Humidity'].values
pres_data = pres_df['Pressure'].values

# Prepare data for each dataset
X_temp, y_temp, temp_scaler = prepare_data(temp_data)
X_hum, y_hum, hum_scaler = prepare_data(hum_data)
X_pres, y_pres, pres_scaler = prepare_data(pres_data)

# Reshape data for LSTM input 
X_temp = np.reshape(X_temp, (X_temp.shape[0], 10, 1))
X_hum = np.reshape(X_hum, (X_hum.shape[0], 10, 1))
X_pres = np.reshape(X_pres, (X_pres.shape[0], 10, 1))

# Define LSTM model
def create_model():
    model = Sequential()
    model.add(LSTM(50, input_shape=(10, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

# Create and train models
model_temp = create_model()
model_temp.fit(X_temp, y_temp, epochs=10, batch_size=1, verbose=2)

model_hum = create_model()
model_hum.fit(X_hum, y_hum, epochs=10, batch_size=1, verbose=2)

model_pres = create_model()
model_pres.fit(X_pres, y_pres, epochs=10, batch_size=1, verbose=2)

# Save the mdoels
os.makedirs("models", exist_ok=True)
model_temp.save("models/temp_model.h5")
model_hum.save("models/hum_model.h5")
model_pres.save("models/pres_model.h5")

# Load models for prediction
loaded_temp_model = load_model("models/temp_model.h5")
loaded_hum_model = load_model("models/hum_model.h5")
loaded_pres_model = load_model("models/pres_model.h5")

############ PREDICTING THE FINAL VALUE ########################### 

def predict_next_value(model, scaler, input_data):
    input_data_scaled = scaler.transform(np.array(input_data).reshape(-1, 1))
    input_data_reshaped = np.reshape(input_data_scaled, (1, 10, 1))
    prediction_scaled = model.predict(input_data_reshaped)
    prediction = scaler.inverse_transform(prediction_scaled)
    return prediction[0][0]

input_temp = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
input_hum = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
input_pres = [1010, 1009, 1008, 1007, 1006, 1005, 1004, 1003, 1002, 1001]

next_temp = predict_next_value(loaded_temp_model, temp_scaler, input_temp)
next_hum = predict_next_value(loaded_hum_model, hum_scaler, input_hum)
next_pres = predict_next_value(loaded_pres_model, pres_scaler, input_pres)

print("Predicted next temperature:", next_temp)
print("Predicted next humidity:", next_hum)
print("Predicted next pressure:", next_pres)
