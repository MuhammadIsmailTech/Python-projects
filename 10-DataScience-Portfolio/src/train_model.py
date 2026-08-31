import os
from sklearn.linear_model import LinearRegression
import joblib
from src.data_cleaning import load_data, clean_data
from src.feature_engineering import add_features

def train(save_path='model/trained_model.pkl'):
    df = load_data()
    df = clean_data(df)
    df = add_features(df)
    X = df[['Rooms','Area','Location_code']]
    y = df['Price']
    model = LinearRegression().fit(X,y)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)
    print('Model saved to', save_path)

if __name__ == '__main__':
    train()
