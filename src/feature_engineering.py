import pandas as pd
import os

def build_lag_feature(file=None, start="2025-01-01", end="2025-12-31"):
    if file is None:
        raise ValueError("The file is invalid.")
    cleaned_data = pd.read_csv(file)
    cleaned_data['datetime']=pd.to_datetime(cleaned_data['datetime'],errors='coerce')
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    mask = (cleaned_data['datetime']>=start) & (cleaned_data['datetime']<end)
    cleaned_data = cleaned_data[mask]

    lag = pd.DataFrame()
    
    features = ['snowdepth', 'tempmin', 'tempmax', 'solarradiation', 'solarenergy', 'sealevelpressure']
    for col in features:
        for i in range(3):
            lag[f'{col}_lag{i+1}'] = cleaned_data[col].shift(periods=i+1)
    
    lag_data = pd.concat(objs=[cleaned_data,lag], axis=1)
    lag_data.dropna(inplace=True)
    
    lag_data.to_csv(os.path.join("./data/lag_features/", f"{start.date()}_{end.date()}_weather_lagged.csv"), index=False)
    return lag_data