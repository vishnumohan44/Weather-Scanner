from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load the data
data = pd.read_csv('seattle-weather.csv')

# Separate features and target
X = data[['precipitation', 'temp_max', 'temp_min', 'wind']]
y = data['weather']

# Manually encode the classes
class_mapping = {'drizzle': 0, 'rain': 1, 'sun': 2, 'snow': 3, 'fog': 4}
inverse_class_mapping = {v: k for k, v in class_mapping.items()}
y_encoded = y.map(class_mapping)

# Initialize the model
model = RandomForestClassifier()
model.fit(X, y_encoded)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get input values from the form
        precipitation = float(request.form['precipitation'])
        temp_max = float(request.form['temp_max'])
        temp_min = float(request.form['temp_min'])
        wind = float(request.form['wind'])

        # Make a prediction
        input_data = [[precipitation, temp_max, temp_min, wind]]
        predicted_label = model.predict(input_data)
        predicted_weather = inverse_class_mapping[predicted_label[0]]

        return render_template('index.html', prediction=predicted_weather)

if __name__ == '__main__':
    app.run(debug=True)
