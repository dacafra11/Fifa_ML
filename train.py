import os
import glob
import pandas as pd
import missingno as msno
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from lightgbm import LGBMRegressor
from sklearn.model_selection import GridSearchCV
import joblib 

os.chdir("C:\\src\\model\\") 
df_Fifa = pd.read_csv("my_model_FOT.csv")

train=df_Fifa
X = train.drop(['Overall'], axis=1)
y = train['Overall'].copy()
X.shape
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

hyper_parametros_lightgbm = {'num_leaves': [50,100],
    'max_depth': [5,10],
    'min_data_in_leaf': [20,100]}
grid=GridSearchCV(estimator=LGBMRegressor(),
param_grid=hyper_parametros_lightgbm,n_jobs=-1,scoring='neg_mean_absolute_error')

lightgbm = grid.fit(X_train,y_train)
prediction_lightgbm = lightgbm.predict(X_test)

joblib.dump(lightgbm, 'C:\\src\\model\\modelo_entrenado_fot2.pkl') # Guardo el modelo.   
