import pandas as pd

def load_data(path="data/housing.csv"):
    df = pd.read_csv(path)
    return df

def clean_data(df):
    df = df.copy()
    df['Location'] = df['Location'].str.strip()
    df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
    df['Rooms'] = pd.to_numeric(df['Rooms'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna()
    return df

if __name__ == '__main__':
    df = load_data()
    print(df.head())
    print('Cleaned:')
    print(clean_data(df).head())
