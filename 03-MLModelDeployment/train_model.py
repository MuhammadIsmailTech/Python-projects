import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Step 1: Load dataset
data = pd.read_csv('data/housing.csv')

# Step 2: Encode location (convert text to numbers)
data['Location'] = data['Location'].map({'Urban': 2, 'Suburban': 1, 'Rural': 0})

# Step 3: Define features and target
X = data[['Rooms', 'Area', 'Location']]
y = data['Price']

# Step 4: Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 6: Save model
pickle.dump(model, open('model/model.pkl', 'wb'))

print("Model trained and saved successfully!")
