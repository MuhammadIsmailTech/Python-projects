# ============================================
# California House Price Prediction
# Model Training Script
# ============================================

import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================
# 1. LOAD DATASET
# ============================================

DATA_PATH = "data/housing.csv"

data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", data.shape)
print()


# ============================================
# 2. CREATE FEATURES
# ============================================

# Bedroom ratio:
# How many bedrooms exist compared with total rooms
data["bedroom_ratio"] = (
    data["total_bedrooms"] / data["total_rooms"]
)

# Rooms per household:
# How many rooms exist per household
data["rooms_per_household"] = (
    data["total_rooms"] / data["households"]
)


# ============================================
# 3. SEPARATE FEATURES AND TARGET
# ============================================

X = data.drop("median_house_value", axis=1)

y = data["median_house_value"]


# ============================================
# 4. TRAIN-TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print()


# ============================================
# 5. IDENTIFY COLUMN TYPES
# ============================================

numeric_features = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income",
    "bedroom_ratio",
    "rooms_per_household"
]

categorical_features = [
    "ocean_proximity"
]


# ============================================
# 6. NUMERICAL PREPROCESSING
# ============================================

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)


# ============================================
# 7. CATEGORICAL PREPROCESSING
# ============================================

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


# ============================================
# 8. COMBINE PREPROCESSING
# ============================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_transformer,
            numeric_features
        ),
        (
            "categorical",
            categorical_transformer,
            categorical_features
        )
    ]
)


# ============================================
# 9. LINEAR REGRESSION MODEL
# ============================================

linear_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            LinearRegression()
        )
    ]
)

print("Training Linear Regression...")

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)

linear_rmse = mean_squared_error(
    y_test,
    linear_predictions
) ** 0.5

linear_r2 = r2_score(
    y_test,
    linear_predictions
)

print("Linear Regression Results")
print("-------------------------")
print("MAE :", round(linear_mae, 2))
print("RMSE:", round(linear_rmse, 2))
print("R2  :", round(linear_r2, 4))
print()


# ============================================
# 10. RANDOM FOREST MODEL
# ============================================

random_forest_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

print("Training Random Forest...")

random_forest_model.fit(X_train, y_train)

forest_predictions = random_forest_model.predict(X_test)

forest_mae = mean_absolute_error(
    y_test,
    forest_predictions
)

forest_rmse = mean_squared_error(
    y_test,
    forest_predictions
) ** 0.5

forest_r2 = r2_score(
    y_test,
    forest_predictions
)

print("Random Forest Results")
print("---------------------")
print("MAE :", round(forest_mae, 2))
print("RMSE:", round(forest_rmse, 2))
print("R2  :", round(forest_r2, 4))
print()


# ============================================
# 11. COMPARE MODELS
# ============================================

print("================================")
print("MODEL COMPARISON")
print("================================")

print(
    f"Linear Regression R2: {linear_r2:.4f}"
)

print(
    f"Random Forest R2:     {forest_r2:.4f}"
)

print()


# ============================================
# 12. SELECT BEST MODEL
# ============================================

if forest_r2 > linear_r2:
    best_model = random_forest_model
    best_model_name = "Random Forest"
    best_score = forest_r2

else:
    best_model = linear_model
    best_model_name = "Linear Regression"
    best_score = linear_r2


print("Best Model:", best_model_name)
print("Best R2 Score:", round(best_score, 4))


# ============================================
# 13. CREATE MODELS DIRECTORY
# ============================================

os.makedirs("models", exist_ok=True)


# ============================================
# 14. SAVE BEST MODEL
# ============================================

MODEL_PATH = "models/house_price_model.pkl"

joblib.dump(
    best_model,
    MODEL_PATH
)

print()
print("Model saved successfully!")
print("Location:", MODEL_PATH)