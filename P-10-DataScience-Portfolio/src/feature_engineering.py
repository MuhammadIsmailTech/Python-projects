def add_features(df):
    df = df.copy()
    mapping = {'Rural':0,'Suburban':1,'Urban':2}
    df['Location_code'] = df['Location'].map(mapping)
    df['Price_per_sqft'] = df['Price'] / df['Area']
    return df

if __name__ == '__main__':
    import pandas as pd
    from src.data_cleaning import load_data, clean_data
    df = load_data()
    df = clean_data(df)
    df = add_features(df)
    print(df.head())
