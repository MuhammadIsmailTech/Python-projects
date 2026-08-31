import streamlit as st
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
 
# PAGE CONFIGURATION

st.set_page_config(
    page_title="California House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOAD DATA

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/housing.csv"
    )

# LOAD MODEL
 
# LOAD MODEL

@st.cache_resource
def load_model(data):

    # Create engineered features
    model_data = data.copy()

    model_data["bedroom_ratio"] = (
        model_data["total_bedrooms"] /
        model_data["total_rooms"]
    )

    model_data["rooms_per_household"] = (
        model_data["total_rooms"] /
        model_data["households"]
    )

    # Features
    X = model_data.drop(
        "median_house_value",
        axis=1
    )

    # Target
    y = model_data["median_house_value"]

    # Numerical features
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

    # Categorical features
    categorical_features = [
        "ocean_proximity"
    ]

    # Numerical preprocessing
    numeric_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            )
        ]
    )

    # Categorical preprocessing
    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
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

    # Combine preprocessing
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

    # Random Forest model
    model = Pipeline(
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

    # Train model
    model.fit(X, y)

    return model


data = load_data()
model = load_model(data)

# PAGE STYLE

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .prediction-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .prediction-value {
        font-size: 42px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# SIDEBAR NAVIGATION

st.sidebar.title("🏠 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Price Prediction",
        "📊 Dashboard",
        "ℹ️ About Project"
    ]
)

# SIDEBAR MODEL INFORMATION

st.sidebar.divider()

st.sidebar.subheader("🤖 Model Information")

st.sidebar.write(
    "**Algorithm:** Random Forest Regressor"
)

st.sidebar.write(
    "**R² Score:** 81.59%"
)

st.sidebar.write(
    "**MAE:** $31,737"
)

st.sidebar.write(
    "**RMSE:** $49,111"
)

# PAGE 1 - PRICE PREDICTION

if page == "🏠 Price Prediction":

    st.markdown(
        '<div class="main-title">'
        '🏠 California House Price Predictor'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Machine Learning based house price prediction system'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📍 Location Information'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        longitude = st.number_input(
            "Longitude",
            min_value=-125.0,
            max_value=-114.0,
            value=-118.0,
            step=0.01
        )

    with col2:

        latitude = st.number_input(
            "Latitude",
            min_value=32.0,
            max_value=42.0,
            value=34.0,
            step=0.01
        )


    # -----------------------------------------------------
    # PROPERTY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏠 Property Information'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        housing_median_age = st.number_input(
            "Housing Median Age",
            min_value=1.0,
            max_value=100.0,
            value=25.0,
            step=1.0
        )

    with col2:

        total_rooms = st.number_input(
            "Total Rooms",
            min_value=1.0,
            max_value=50000.0,
            value=2000.0,
            step=100.0
        )

    with col3:

        total_bedrooms = st.number_input(
            "Total Bedrooms",
            min_value=1.0,
            max_value=10000.0,
            value=400.0,
            step=50.0
        )


    # -----------------------------------------------------
    # POPULATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '👨‍👩‍👧 Population Information'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        population = st.number_input(
            "Population",
            min_value=1.0,
            max_value=50000.0,
            value=1000.0,
            step=100.0
        )

    with col2:

        households = st.number_input(
            "Households",
            min_value=1.0,
            max_value=10000.0,
            value=400.0,
            step=50.0
        )

    with col3:

        median_income = st.number_input(
            "Median Income",
            min_value=0.1,
            max_value=20.0,
            value=4.0,
            step=0.1
        )


    # -----------------------------------------------------
    # OCEAN PROXIMITY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🌊 Ocean Proximity'
        '</div>',
        unsafe_allow_html=True
    )

    ocean_proximity = st.selectbox(
        "Select the location category",
        [
            "<1H OCEAN",
            "INLAND",
            "ISLAND",
            "NEAR BAY",
            "NEAR OCEAN"
        ]
    )


    st.divider()


    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------

    predict_button = st.button(
        "🔮 Predict House Price",
        use_container_width=True,
        type="primary"
    )


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    if predict_button:

        if total_rooms <= 0:

            st.error(
                "Total rooms must be greater than zero."
            )

            st.stop()


        if households <= 0:

            st.error(
                "Households must be greater than zero."
            )

            st.stop()


        # Feature engineering

        bedroom_ratio = (
            total_bedrooms / total_rooms
        )

        rooms_per_household = (
            total_rooms / households
        )

        # Create input DataFrame

        input_data = pd.DataFrame({

            "longitude": [longitude],

            "latitude": [latitude],

            "housing_median_age": [
                housing_median_age
            ],

            "total_rooms": [
                total_rooms
            ],

            "total_bedrooms": [
                total_bedrooms
            ],

            "population": [
                population
            ],

            "households": [
                households
            ],

            "median_income": [
                median_income
            ],

            "ocean_proximity": [
                ocean_proximity
            ],

            "bedroom_ratio": [
                bedroom_ratio
            ],

            "rooms_per_household": [
                rooms_per_household
            ]
        })


        # Make prediction

        prediction = model.predict(
            input_data
        )[0]

        # Display prediction

        st.success(
            "Prediction completed successfully!"
        )

        st.markdown(
            '<div class="prediction-box">',
            unsafe_allow_html=True
        )

        st.subheader(
            "💰 Estimated Median House Value"
        )

        st.markdown(
            f'<div class="prediction-value">'
            f'${prediction:,.0f}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # Additional information

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Bedroom Ratio",
                f"{bedroom_ratio:.2f}"
            )

        with col2:

            st.metric(
                "Rooms / Household",
                f"{rooms_per_household:.2f}"
            )

        with col3:

            st.metric(
                "Ocean Proximity",
                ocean_proximity
            )


        # Show input data

        with st.expander(
            "🔎 View Input Information"
        ):

            st.dataframe(
                input_data,
                use_container_width=True
            )

# PAGE 2 - DASHBOARD

elif page == "📊 Dashboard":

    st.title(
        "📊 California Housing Dataset Dashboard"
    )

    st.write(
        "Explore the dataset and understand the "
        "Machine Learning model."
    )


    # -----------------------------------------------------
    # DATASET METRICS
    # -----------------------------------------------------

    st.subheader(
        "📌 Dataset Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Records",
            f"{len(data):,}"
        )

    with col2:

        st.metric(
            "Total Features",
            data.shape[1]
        )

    with col3:

        missing_values = data.isnull().sum().sum()

        st.metric(
            "Missing Values",
            missing_values
        )

    with col4:

        st.metric(
            "Target Average",
            f"${data['median_house_value'].mean():,.0f}"
        )


    st.divider()


    # -----------------------------------------------------
    # DATASET PREVIEW
    # -----------------------------------------------------

    st.subheader(
        "🔍 Dataset Preview"
    )

    st.dataframe(
        data.head(20),
        use_container_width=True
    )


    # -----------------------------------------------------
    # MISSING VALUES
    # -----------------------------------------------------

    st.subheader(
        "⚠️ Missing Values"
    )

    missing_data = (
        data.isnull()
        .sum()
        .reset_index()
    )

    missing_data.columns = [
        "Column",
        "Missing Values"
    ]

    missing_data = missing_data[
        missing_data["Missing Values"] > 0
    ]

    if len(missing_data) > 0:

        st.dataframe(
            missing_data,
            use_container_width=True
        )

    else:

        st.success(
            "No missing values found."
        )


    # -----------------------------------------------------
    # TARGET DISTRIBUTION
    # -----------------------------------------------------

    st.subheader(
        "💰 House Value Distribution"
    )

    st.bar_chart(
        data["median_house_value"]
        .value_counts()
        .sort_index()
        .head(100)
    )


    # -----------------------------------------------------
    # CORRELATION
    # -----------------------------------------------------

    st.subheader(
        "🔗 Feature Correlation"
    )

    numeric_data = data.select_dtypes(
        include=np.number
    )

    correlation = (
        numeric_data
        .corr()
        ["median_house_value"]
        .sort_values(
            ascending=False
        )
    )

    st.dataframe(
        correlation.reset_index()
        .rename(
            columns={
                "index": "Feature",
                "median_house_value": "Correlation"
            }
        ),
        use_container_width=True
    )


    # -----------------------------------------------------
    # MODEL PERFORMANCE
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "🤖 Model Performance"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Random Forest R²",
            "81.59%"
        )

    with col2:

        st.metric(
            "MAE",
            "$31,737"
        )

    with col3:

        st.metric(
            "RMSE",
            "$49,111"
        )


    st.info(
        "Random Forest was selected as the final model "
        "because it achieved a higher R² score than "
        "Linear Regression in our evaluation."
    )


# PAGE 3 - ABOUT


elif page == "ℹ️ About Project":

    st.title(
        "ℹ️ About This Project"
    )

    st.write(
        """
        ### California House Price Prediction

        This project uses Machine Learning to predict
        the median house value of a housing block in
        California.

        The system uses information such as:

        - Geographic location
        - Housing age
        - Number of rooms
        - Number of bedrooms
        - Population
        - Number of households
        - Median income
        - Ocean proximity

        Two Machine Learning algorithms were evaluated:

        1. Linear Regression
        2. Random Forest Regression

        Random Forest achieved the better performance
        in our evaluation and was selected as the final
        prediction model.
        """
    )


    st.divider()

    st.subheader(
        "🛠️ Technologies Used"
    )

    technologies = pd.DataFrame({

        "Technology": [
            "Python",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Streamlit",
            "Joblib"
        ],

        "Purpose": [
            "Programming Language",
            "Data Processing",
            "Numerical Operations",
            "Machine Learning",
            "User Interface",
            "Model Saving"
        ]
    })

    st.dataframe(
        technologies,
        use_container_width=True
    )


    st.divider()

    st.subheader(
        "📈 Final Model"
    )

    st.write(
        "**Random Forest Regressor**"
    )

    st.write(
        "R² Score: **81.59%**"
    )

    st.write(
        "MAE: **$31,737**"
    )

    st.write(
        "RMSE: **$49,111**"
    )

# FOOTER

st.divider()

st.caption(
    "California House Price Predictor | "
    "Machine Learning University Project"
)