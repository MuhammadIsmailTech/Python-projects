# 🏠 California House Price Predictor

A Machine Learning web application that predicts the median house value of a California housing block based on housing, demographic, income, and geographical information.

The project uses **Random Forest Regression** as the final prediction model and **Streamlit** to provide a user-friendly web interface.

##  Project Overview

House prices depend on several factors such as location, income, number of rooms, number of bedrooms, population, and proximity to the ocean.

This project uses historical California housing data to train Machine Learning models and predict the median house value for new housing information.

Two regression models were trained and compared:

* Linear Regression
* Random Forest Regression

After evaluation, Random Forest was selected as the final model because it produced better results.

## 🎯 Project Objectives

* Load and analyze the California housing dataset.
* Handle missing values.
* Process categorical data.
* Perform feature engineering.
* Train Machine Learning regression models.
* Compare model performance.
* Select the best-performing model.
* Save the trained model.
* Build a user-friendly Streamlit application.
* Allow users to make house-price predictions.

## 📊 Dataset

The dataset contains:

* **20,640 records**
* **10 original features**

### Features

| Feature            | Description                     |
| ------------------ | ------------------------------- |
| longitude          | Geographical longitude          |
| latitude           | Geographical latitude           |
| housing_median_age | Median age of houses            |
| total_rooms        | Total number of rooms           |
| total_bedrooms     | Total number of bedrooms        |
| population         | Population of the housing block |
| households         | Number of households            |
| median_income      | Median income                   |
| median_house_value | Target variable                 |
| ocean_proximity    | Proximity to the ocean          |

The target variable is:

```text
median_house_value
```

## 🧹 Data Preprocessing

The project performs several preprocessing operations.

### Missing Values

The `total_bedrooms` column contains missing values.

Median imputation is used to handle these missing values.

### Categorical Encoding

The `ocean_proximity` column contains categorical values.

One-Hot Encoding is used to convert these categories into numerical features.

### Feature Engineering

Two additional features are created:

```text
bedroom_ratio = total_bedrooms / total_rooms
```

and

```text
rooms_per_household = total_rooms / households
```

##  Machine Learning Models

### 1. Linear Regression

Linear Regression was used as the baseline model.

### 2. Random Forest Regression

Random Forest Regression was used as the second model and achieved better performance.

Therefore, Random Forest was selected as the final prediction model.

## 📈 Model Performance

The models were evaluated using:

* MAE — Mean Absolute Error
* RMSE — Root Mean Squared Error
* R² — R-squared score

| Model             |        MAE |       RMSE |         R² |
| ----------------- | ---------: | ---------: | ---------: |
| Linear Regression | $49,642.62 | $69,131.85 |     0.6353 |
| Random Forest     | $31,736.63 | $49,110.75 | **0.8159** |

### Final Model

**Random Forest Regression**

```text
R² Score: 0.8159
MAE: $31,736.63
RMSE: $49,110.75
```

## 🖥️ User Interface

The project includes a Streamlit web application.

The application contains:

### Price Prediction

Users can enter:

* Longitude
* Latitude
* Housing median age
* Total rooms
* Total bedrooms
* Population
* Households
* Median income
* Ocean proximity

The application then generates an estimated median house value.

### Dashboard

The dashboard provides information such as:

* Dataset size
* Number of features
* Missing values
* Dataset preview
* Target distribution
* Correlation information
* Model performance

### About Project

This page provides information about the project, Machine Learning models, and technologies used.

##  Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Streamlit
* Visual Studio Code
* Git
* GitHub

##  Project Structure

```text
California-House-Price-Predictor/
│
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── housing.csv
│
├── models/
│   └── house_price_model.pkl
│
└── notebooks/
```

## ⚙️ Installation

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd California-House-Price-Predictor
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Project

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your web browser.

## Train the Model

If you want to train the Machine Learning model again, run:

```bash
python train_model.py
```

The trained model will be saved in:

```text
models/house_price_model.pkl
```

---

## Important Note

This project provides an estimated median house value based on patterns learned from the California housing dataset.

It is **not a live real-estate valuation system** and does not use current property-market prices.

## Future Improvements

Possible future improvements include:

* Hyperparameter tuning.
* Cross-validation.
* Interactive maps.
* More visualizations.
* Feature importance analysis.
* Prediction history.
* Online deployment.
* User authentication.
* Live housing-market data.

##  Author

**Name:** Muhammad Ismail

**Project:** California House Price Prediction

**Type:** Machine Learning / Data Science Project


## Project Result

The final Random Forest model achieved an **R² score of 0.8159** on the project's test set and was selected as the final prediction model.

The model was integrated into a Streamlit application to provide a simple and user-friendly prediction interface.
