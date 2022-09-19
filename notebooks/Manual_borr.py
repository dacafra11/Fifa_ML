# importing necessary libraries and functions
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, url_for, redirect
import pickle
import joblib
import lightgbm as lgb
from lightgbm import LGBMRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from utility import utils2 as u 
import seaborn as sns
import missingno as msno
import openpyxl
import urllib.request
from PIL import Image
import os

os.chdir(os.path.dirname(__file__))
app = Flask(__name__) #Initialize the flask App
#model = pickle.load(open('modelo_entrenado_fot.pkl', 'rb')) # loading the trained model

model=joblib.load('/src/model/modelo_entrenado_fot.pkl')
#model=pickle.load('modelo_entrenado_fot.pkl')

def prediction(s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,s_15,model): 
    pre_data = np.array([s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,s_15]) 
    pre_data_reshape = pre_data.reshape(1, -1) 
    pred_result = model.predict(pre_data_reshape)  

    return pred_result[0]
 

@app.route('/')
def input_data(): 

    return render_template('Pred_m.html') 

@app.route('/result', methods=["POST", "GET"]) 
def input(): 
    if request.method == "POST": 
        s_1 = request.form['s_1']
        s_2 = request.form['s_2']
        s_3 = request.form['s_3']
        s_4 = request.form['s_4']
        s_5 = request.form['s_5']
        s_6 = request.form['s_6']
        s_7 = request.form['s_7']
        s_8 = request.form['s_8']
        s_9 = request.form['s_9']
        s_10 = request.form['s_10']
        s_11 = request.form['s_11']
        s_12 = request.form['s_12']
        s_13 = request.form['s_13']
        s_14 = request.form['s_14']
        s_15 = request.form['s_15']

        predicted_result = prediction(s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,s_15,model)  

        predicted_result = round(predicted_result,2)
        predicted_result=int(predicted_result)
        predicted_result=str(predicted_result)
        
        return render_template('Pred_resul.html', predicted = predicted_result) 

if __name__ == "__main__":
    app.run(debug=True)