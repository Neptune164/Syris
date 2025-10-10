import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from joblib import dump
import os



def hybrid_model(file=None, test_time='2025-06-01'):
    if file is None:
        raise ValueError("The file is invalid.")
    
    df = pd.read_csv(file)
    df['datetime']=pd.to_datetime(df['datetime'], errors="coerce")
    ################## Train-Test split ##########################
    cutoff = pd.to_datetime(test_time)
    df_train = df[df['datetime']<cutoff].copy()
    df_val = df[df['datetime']>=cutoff].copy()

    X_train = df_train.drop(columns=["temp","datetime"])
    y_train = df_train["temp"]
    X_val = df_val.drop(columns=["temp","datetime"])
    y_val = df_val["temp"]

    ################# Training on XGB & RF ###################### 
    params_GB = {'n_estimators': 100, 'max_depth':3, 'learning_rate': 1.0}
    GB = XGBRegressor(n_estimators=params_GB['n_estimators'],
                      max_depth=params_GB['max_depth'],
                      learning_rate=params_GB['learning_rate'])
    GB.fit(X=X_train, y=y_train)
    pred_GB = GB.predict(X_train)
    residual = y_train - pred_GB

    params_RF = {'n_estimators': 100, 'max_depth':20, 'max_features': 1.0}
    RF = RandomForestRegressor(random_state=42,
                                n_estimators=params_RF['n_estimators'],
                               max_depth=params_RF['max_depth'],
                               max_features=params_RF['max_features'],
                               criterion='absolute_error')
    RF.fit(X=X_train, y=residual)
    final_pred = GB.predict(X_val) + RF.predict(X_val)

    ################## Results ###################
    mae = mean_absolute_error(y_val, final_pred)
    r2 = r2_score(y_val, final_pred)
    mape = np.mean(np.abs(y_val-final_pred)/y_val)*100

    print("Training sucessfully!")
    print(f"MAE = {mae:.2f}")
    print(f"R square = {r2:.2f}")
    print(f"MAPE = {mape:.2f}")

    dump(GB, os.path.join(f"./models/xgboost_{params_GB['n_estimators']}_{params_GB['max_depth']}_{params_GB['learning_rate']}.pkl"))
    dump(RF, os.path.join(f"./models/rf_{params_RF['n_estimators']}_{params_RF['max_depth']}_{params_RF['max_features']}.pkl"))