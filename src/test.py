import joblib
import os
from feature_engineering import build_lag_feature
from data_processing import preprocessing

# load models
rf_model = "./models/rf_100_20_1.0.pkl"
xgb_model = "./models/xgboost_100_3_1.0.pkl"
dirFile = "./data/raw/Syracuse_last15days.csv"
tarPath = "./data/cleaned"
filename = "09-24_10-10"

RF = joblib.load(os.path.join(rf_model))
GB = joblib.load(os.path.join(xgb_model))

preprocessing(os.path.join(dirFile), os.path.join(tarPath), filename)
