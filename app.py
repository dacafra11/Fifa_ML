#! -*- conding: utf-8 -*-
#from flask_menu import Menu, register_menu
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, url_for, redirect
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
from werkzeug.utils import secure_filename 
import os 

app = Flask(__name__)

os.chdir(os.path.dirname(__file__))

@app.route('/')
def input_data(): 
    return render_template('index.html') 


model=joblib.load('./model/modelo_entrenado_fot.pkl')
# redondear y modificart reshape
def prediction(s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,model): 
    pre_data = np.array([s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14]) 
    pre_data_reshape = pre_data.reshape(1, -1) 
    pred_result = model.predict(pre_data_reshape)  
    return pred_result[0]
 
@app.route('/result', methods=["POST", "GET"]) 

def input(): 
    
    
    if request.method == "POST": 
        s_1 = float(request.form['s_1'])
        s_2 = float(request.form['s_2'])
        s_3 = float(request.form['s_3'])
        s_4 = float(request.form['s_4'])
        s_5 = float(request.form['s_5'])
        s_6 = float(request.form['s_6'])
        s_7 = float(request.form['s_7'])
        s_8 = float(request.form['s_8'])
        s_9 = float(request.form['s_9'])
        s_10 = float(request.form['s_10'])
        s_11 = float(request.form['s_11'])
        s_12 = float(request.form['s_12'])
        s_13 = float(request.form['s_13'])
        s_14 = float(request.form['s_14'])

        predicted_result = prediction(s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,model)  
         
        predicted_result = round(predicted_result,2)
        predicted_result=int(predicted_result)
        predicted_result=str(predicted_result)
        return render_template('Pred_resul.html', predicted = predicted_result) 
    return render_template('Pred_m.html')

# Limpia y genera el modelo de entrenamiento y guarda a csv el modelo de df
# para usar en automatico y manual.
@app.route("/result2", methods=['POST','GET'])
def uploadFiles():
      # get the uploaded file
    
       if request.method == "POST": 
        return render_template('Pred_a.html')
       else:
        #return render_template('Limp.html')
         uploaded_file = request.files['file']
         if uploaded_file.filename != '':
       
           data_Fifa = pd.read_csv(request.files.get('file'))

           data_Fifa =u.modificar_dataframe(data_Fifa)
           data_Fifa=u.borrar(data_Fifa)
           data_Fifa=u.normalizar_categor(data_Fifa)
           data_Fifa= data_Fifa.round(2)
           data_Fifa.to_csv("./model/my_model_FOT.csv", sep=',', encoding="utf-8", index=False)
           table = data_Fifa.to_html(index=False)
           u.entrena_modelo(data_Fifa)
           return render_template('contact.html', 
                            shape = data_Fifa.shape,
                            table = table)
    # # #   return redirect(url_for('Limp'))
    #    return render_template('Limp.html')

@app.route("/contact", methods=['POST','GET'])
def contact():
      return render_template('contact.html')

# Entrene automatico
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   #model=joblib.load('./model/modelo_entrenado_fot.pkl') #se deberia poder eliminar
   if request.method == 'POST':
      df =  pd.read_csv("./model/my_model_FOT.csv")
      df= df.drop(["Overall"], axis =1)
      predicted_result2 = df.sample()
      pred_result2 = model.predict(predicted_result2)
      pred_result2=int(pred_result2)
      pred_result2 = round(pred_result2,2)
      pred_result2=str(pred_result2)        
      return render_template('Pred_resul.html', predicted = pred_result2)
   return render_template('Pred_a.html')  



if __name__ == '__main__':
    app.run(debug=True)