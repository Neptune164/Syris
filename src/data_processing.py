import pandas as pd
import os

def preprocessing(dirFile, tarPath, fileName):
    keep_features = ["datetime","temp", "tempmax", "tempmin", 
                     "precip","snowdepth","snow","solarenergy","solarradiation",
                     "uvindex","cloudcover","sealevelpressure"]
    raw_data = pd.read_csv(dirFile)
    features = raw_data.columns
    drop_features = [x for x in features if x not in keep_features]
    raw_data = raw_data.drop(columns=drop_features)
    
    # print(raw_data.isna().sum())
    raw_data = raw_data.dropna()
    raw_data.to_csv(os.path.join(tarPath, f"{fileName}_weather_cleaned.csv"), index=False)