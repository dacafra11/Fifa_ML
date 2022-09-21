import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
import missingno as msno
import openpyxl
import sklearn
from sklearn.model_selection import KFold, cross_val_score, train_test_split
import lightgbm as lgb
from lightgbm import LGBMRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold, cross_val_score, train_test_split
import joblib 

warnings.filterwarnings('ignore') # Para evitar los molestos avisos.

def modificar_dataframe(data_Fifa):
    """ Función modificación de datos, creación de variables temporales 
        y borrado de columnas sin uso para ambos dataframes
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos limpiar/borrar/modificar_columnas

    Parameters
    ----------
    parametro_2 : dataframe
    Dataframe que deseamos limpiar/borrar/modificar_columnas

    Returns
    -------
    dataframe1, dataframe2
    Devuelve dos dataframe con datos modificados y genera un csv como punto de control
    """
    #data_Fifa = data_Fifa.drop(data_Fifa[data_Fifa['Pais']=="Borrar"].index) 
    data_Fifa.columns = data_Fifa.columns.str.replace(' ', '_') 
    #Valores de las cartas de los jugadores de campo
    data_Fifa['Def_Awareness']= 0
    data_Fifa['Def_Awareness'][(data_Fifa['Marking'].notnull())]=data_Fifa['Marking']
    #data_Fifa['Def_Awareness'][(data_Fifa['DefensiveAwareness'].notnull())]=data_Fifa['DefensiveAwareness']
    data_Fifa['PAC']=0
    data_Fifa['PAC'][(data_Fifa['Best_Position'] != "GK")]=(data_Fifa['Acceleration'] + data_Fifa['SprintSpeed'])/2
    data_Fifa['SHO']=0
    data_Fifa['SHO'][(data_Fifa['Best_Position'] != "GK")]=(data_Fifa['Finishing'] + data_Fifa['Volleys']+ data_Fifa['ShotPower'] + data_Fifa['LongShots']+ data_Fifa['Positioning'] + data_Fifa['Penalties'] )/6
    data_Fifa['PAS']=0
    data_Fifa['PAS'][(data_Fifa['Best_Position'] != "GK")]=(data_Fifa['Crossing'] + data_Fifa['ShortPassing']+ data_Fifa['Curve'] + data_Fifa['FKAccuracy']+ data_Fifa['LongPassing'] + data_Fifa['Vision'] )/6
    data_Fifa['DRI']=0
    data_Fifa['DRI'][(data_Fifa['Best_Position'] != "GK")]=(data_Fifa['Dribbling'] + data_Fifa['BallControl']+ data_Fifa['Balance'] + data_Fifa['Agility']+ data_Fifa['Reactions'] + data_Fifa['Composure'] )/6
    data_Fifa['DEF']=0
    data_Fifa['DEF'][(data_Fifa['Best_Position'] != "GK")]=(data_Fifa['Interceptions'] + data_Fifa['StandingTackle']+ data_Fifa['SlidingTackle'] + data_Fifa['HeadingAccuracy'] + data_Fifa['Def_Awareness'] )/5
    data_Fifa['PHY']=0
    data_Fifa['PHY'][(data_Fifa['Best_Position'] != "GK")]=(data_Fifa['Jumping'] + data_Fifa['Stamina']+ data_Fifa['Strength'] + data_Fifa['Aggression'] )/4
    #Valores de las cartas de los porteros
    data_Fifa=data_Fifa.rename(columns={"GKDiving":"DIV"})
    data_Fifa=data_Fifa.rename(columns={"GKHandling":"HAN"})
    data_Fifa=data_Fifa.rename(columns={"GKKicking":"KIC"})
    data_Fifa=data_Fifa.rename(columns={"GKPositioning":"REF"})
    data_Fifa=data_Fifa.rename(columns={"GKReflexes":"POS"})
    data_Fifa['PAC'][(data_Fifa['Best_Position'] == "GK")]=(data_Fifa['Acceleration'] + data_Fifa['SprintSpeed'])/2
    #Borramos columnas que no vamos a usar en dataframe
    #data_Fifa.drop(columns=("DefensiveAwareness"),inplace=True )
    data_Fifa.drop(columns=("Marking"),inplace=True )
    data_Fifa.drop(columns=("Flag"),inplace=True )
    data_Fifa=data_Fifa.drop(["Vision","Composure","Acceleration","SprintSpeed",
    'Finishing','Volleys','ShotPower','LongShots','Positioning','Penalties',
    'Crossing','ShortPassing','Curve','FKAccuracy','LongPassing','Dribbling',
    'BallControl','Balance','Agility','Reactions','Interceptions',
    'StandingTackle','SlidingTackle','HeadingAccuracy','Def_Awareness',
    'Jumping','Stamina','Strength','Aggression'], axis =1)

       
    return data_Fifa

def borrar(df):
    """ Borramos las columnas con menor incidencia 
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos limpiar/borrar/modificar_columnas

    Returns
    -------
    dataframe1
    Devuelve dataframe con datos modificados
    """
    df=df[(df['Best_Position'] != "GK")]
    df=df.drop(["DIV","HAN","KIC","REF","POS"], axis =1)
    df =df.drop(["Weight","Club","Value","Wage","ID","Photo","Club_Logo",
    "Real_Face","Position","Name","Nationality","Body_Type",
    "Release_Clause","Joined","Contract_Valid_Until","Jersey_Number",
    "Height",'Work_Rate','Loaned_From', 'Best_Position'], axis =1)
    
    return df


def exportar(data_Fifa,data_Real):
    """ Función exportación a csv
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos limpiar/borrar/modificar_columnas

    Parameters
    ----------
    parametro_2 : dataframe
    Dataframe que deseamos limpiar/borrar/modificar_columnas

    Returns
    -------
    dataframe1, dataframe2, dataframe3, dataframe4
    Devuelve 4 dataframe con datos modificados y genera cuatro csv con su contenido
    crearán las tablas de Powerbi, previo paso a excel en funcion conv_xlsx
    """
    data_medidas=data_Fifa.groupby(by=["Club","Year","Pais"]).describe()
    data_medias=data_Fifa.groupby(by=["Club","Year","Pais"]).mean()
    data_medidas.to_csv("data_medidas.csv", sep=',', encoding="utf-8")  #Ojo.32
    data_medias.to_csv("data_medias.csv", sep=',', encoding="utf-8")#Exportamos a csv
    data_Fifa.to_csv("data_Fifa.csv", sep=',', encoding="utf-8", index=False)#Exportamos a csv
    data_Real.to_csv("data_Real.csv", sep=',', encoding="utf-8", index=False)#Exportamos a csv
    return data_Fifa, data_Real, data_medidas, data_medias

def conv_xlsx(file,file2,file3,file4):
    """ Función convierte a xlsx que será origen de datos para PowerBi
    
    Parameters
    ----------
    parametro_1 : file
    Fichero csv para convertir a xlsx

    Parameters
    ----------
    parametro_2 : file
    Fichero csv para convertir a xlsx

    Parameters
    ----------
    parametro_3 : file
    Fichero csv para convertir a xlsx
    
    Parameters
    ----------
    parametro_4 : file
    Fichero csv para convertir a xlsx

    Returns
    -------
    
    Genera 4 xlsx con datos limpiados que serán el origen de datos y crearán 
    las tablas de Powerbi
    """
    pd.read_csv(file).to_excel("data_Fifa.xlsx", index=False)
    pd.read_csv(file2).to_excel("data_Real.xlsx", index=False)
    pd.read_csv(file3).to_excel("data_medias.xlsx", index=False)
    pd.read_csv(file4).to_excel(("data_medidas.xlsx"), index=False)

def normalizar_categor(df):

   
    
    # We convert Categorical to boolean for first dataset
    categorical_feature = (df.drop(columns='Overall').dtypes == "object")

    # filter categorical columns
    categorical_cols = df.drop(columns='Overall').columns[categorical_feature].tolist()

    # Binarize categorical values
    df = pd.get_dummies(df, columns=categorical_cols,
    prefix=categorical_cols, drop_first=True )

    #Normalizamos
    # Min-Max Normalization
    data_Fifa2_1 = df.drop('Overall', axis=1)
    data_Fifa2_norm = (data_Fifa2_1-data_Fifa2_1.min())/(data_Fifa2_1.max()-data_Fifa2_1.min())
    data_Fifa2_norm = pd.concat((data_Fifa2_norm, df.Overall), 1)
    data_Fifa2_norm["Overall"]=df["Overall"]
    df=data_Fifa2_norm
    df=df.fillna(df.mean())

    return df

def entrena_modelo(df_Fifa):
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

    joblib.dump(lightgbm, 'modelo_entrenado_fot.pkl') # Guardo el modelo.    

def prediction(s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,model):
    pre_data = np.array([s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14]) 
    pre_data_reshape = pre_data.reshape(1, -1) 
    pred_result = model.predict(pre_data_reshape)  
    return pred_result[0]