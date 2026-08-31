from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open('model/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    rooms = int(request.form['rooms'])
    area = float(request.form['area'])
    location = request.form['location']

    # Convert location to numeric
    location_map = {'Urban': 2, 'Suburban': 1, 'Rural': 0}
    location_val = location_map.get(location, 0)

    # Prepare data
    features = np.array([[rooms, area, location_val]])

    # Make prediction
    prediction = model.predict(features)[0]

    return render_template('index.html', prediction_text=f"Estimated House Price: ${prediction:,.2f}")

if __name__ == "__main__":
    app.run(debug=True)
