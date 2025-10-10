import pandas as pd
import os

def build_lag_feature(file=None, start=None, end=None):
    if file is None:
        raise ValueError("The file is invalid.")
    
    cleaned_data = pd.read_csv(file)
    cleaned_data['datetime']=pd.to_datetime(cleaned_data['datetime'],errors='coerce')

    if start is None:
        start = cleaned_data['datetime'].iloc[0]

    if end is None:
        end = cleaned_data['datetime'].iloc[-1]

    s = pd.to_datetime(start)
    e = pd.to_datetime(end)
    mask = (cleaned_data['datetime']>=s) & (cleaned_data['datetime']<e)
    filters = cleaned_data[mask]

    lag = pd.DataFrame()
    
    features = ['snowdepth', 'tempmin', 'tempmax', 'solarradiation', 'solarenergy', 'sealevelpressure']
    for col in features:
        for i in range(3):
            lag[f'{col}_lag{i+1}'] = filters[col].shift(periods=i+1)
    
    lag_data = pd.concat(objs=[filters,lag], axis=1)
    lag_data.dropna(inplace=True)
    
    lag_data.to_csv(os.path.join("./data/lag_features/", f"{s.date()}_{e.date()}_weather_lagged.csv"), index=False)
    return lag_data