import joblib
import os
import pandas as pd
from feature_engineering import build_lag_feature
from data_processing import preprocessing

# load models
rf_model = "./models/rf_100_20_1.0.pkl"
xgb_model = "./models/xgboost_100_3_1.0.pkl"

dirFile = "./data/raw/Syracuse_last15days.csv"
tarPath = "./data/cleaned"

cleaned_data = "./data/cleaned/09-24_10-10_weather_cleaned.csv"
start_date = "2025-09-24"
end_date = "2025-09-30"

lag_feature = "./data/lag_features/2025-09-24_2025-09-30_weather_lagged.csv"
filename = "09-24_10-10"

RF = joblib.load(os.path.join(rf_model))
GB = joblib.load(os.path.join(xgb_model))

# preprocessing(os.path.join(dirFile), os.path.join(tarPath), filename)
# build_lag_feature(os.path.join(cleaned_data), start_date, end_date)

date = []
df = pd.read_csv(os.path.join(lag_feature))
df['datetime'] = pd.to_datetime(df['datetime'])
latest = df['datetime'].iloc[-1]
lag = df.drop(columns=['datetime', 'temp'])

preds = GB.predict(lag) + RF.predict(lag)
for i in range(3):
    date.append(latest+pd.Timedelta(days=i+1))

result = pd.DataFrame({
    "datetime": date,
    "temperature": preds
})
print(result)