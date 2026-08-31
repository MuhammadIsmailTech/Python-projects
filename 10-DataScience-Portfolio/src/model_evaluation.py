import joblib
from src.data_cleaning import load_data, clean_data
from src.feature_engineering import add_features
from sklearn.metrics import mean_squared_error, r2_score

def evaluate(model_path='model/trained_model.pkl'):
    model = joblib.load(model_path)
    df = load_data()
    df = clean_data(df)
    df = add_features(df)
    X = df[['Rooms','Area','Location_code']]
    y = df['Price']
    preds = model.predict(X)
    print('MSE', mean_squared_error(y,preds))
    print('R2', r2_score(y,preds))

if __name__ == '__main__':
    evaluate()
