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

warnings.filterwarnings('ignore') # Para evitar los molestos avisos.


def cargar_fichero(file,anyo):
    """ Función carga de ficheros en data frame, añadiendo el año
    
    Parameters
    ----------
    parametro_1 : file
    Fichero que deseamos cargar entre " " con .extension

    parametro_2 : fecha
    Formato fecha "MM/DD/YEAR"

    Returns
    -------
    dataframe
    Devuelve dos dataframes con los datos de los ficheros cargados
    """
    data = pd.concat(map(pd.read_csv, [file]), ignore_index=True) 
    data["Year"]=anyo 
    data["Year"]=pd.to_datetime(data["Year"])

    return data

def peso(df):
    """ Función convierte lbs a kg 
    
    Parameters
    ----------
    parametro_1 : file
    Fichero que deseamos cargar entre " " con .extension
    parametro_2 : 
   

    Returns
    -------
    dataframe
    Devuelve un dataframe con los datos de los ficheros cargados
    """

    d=df.loc[df["Weight"].str.contains('lbs')]
    d["Weight"]=d["Weight"].str.replace('lbs',"")
    d["Weight"]=  d["Weight"].astype(float)
    d['Weight']= round(d['Weight'] * 0.453592,2)

    d2=df.loc[df["Weight"].str.contains('kg')]
    d2["Weight"]=d2["Weight"].str.replace('kg',"")
    d2["Weight"]=  d2["Weight"].astype(float)

    d = pd.concat([d,d2], ignore_index=True)

    df= d

    return df

def altura(df):
    """ Función convierte pie, pulgadas  a cm 
    
    Parameters
    ----------
    parametro_1 : file
    Fichero que deseamos cargar entre " " con .extension
    parametro_2 : 
   

    Returns
    -------
    dataframe
    Devuelve un dataframes con los datos de los ficheros cargados
    """

    d=df.loc[df["Height"].str.contains("'")]
    d["Height"] = d["Height"].str.replace("'",".")
    new = d["Height"].str.split(".", n= 1, expand=True)
    d["Foot"]=new[0]
    d["inc"]=new[1]
    d["Height"] = d["Height"].astype(float)
    d["Foot"]=d["Foot"].astype(float)
    d["inc"]=d["inc"].astype(float)
    d["Foot"]=d["Foot"]*12*2.54
    d["inc"]=d["inc"]*2.54
    d["Height"]= d["Foot"] + d["inc"]

    d2=df.loc[~df["Height"].str.contains("'")]
    d2["Height"]=d2["Height"].str.replace('cm',"")
    d2["Height"]=  d2["Height"].astype(float)

    d = pd.concat([d,d2], ignore_index=True)
    
    df= d

    return df

def concatenar(df1,df2,df3,df4,df5):# kargvs , tendriamos que pasar los 5 ficheros
    """ Función concatena los ficheros  guardadols en sendos dataframes
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos concatenar
    parametro_2 : dataframe
    Dataframe que deseamos concatenar
    .....
    parametro_10 : dataframe
    Dataframe que deseamos concatenar

    Returns
    -------
    dataframe
    Devuelve dos dataframes con los datos concatenados de los 10 df
    """
    dataframe1 =pd.concat([df1,df2,df3,df4,df5], ignore_index=True)
    data_F=dataframe1
    return data_F

def limpiar_df(df):
    """ Función limpia datos distintos del ultimo csv
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos limpiar


    Returns
    -------
    dataframe
    Devuelve dos dataframes con los datos limpios para concatenar con el resto
    """
    df["Value"] = df["Value"].str.replace('$',"")
    df["Value"] = df["Value"].str.replace('M',"")
    df["Value"] = df["Value"].str.replace('€',"")
    df["Value"] = df["Value"].str.replace('K',"")
    df["Wage"] = df["Wage"].str.replace('€',"")
    df["Wage"] = df["Wage"].str.replace('K',"")
    df["Wage"] = df["Wage"].str.replace('M',"")
    df["Club"]=df["Club"].replace(r'[A-Z]{2,3}',"", regex=True) # Borramos todo lo que contenga dos mayusculas consecutivas
    df["Club"]=df["Club"].replace(r'[A-Z]{1}[.]',"", regex=True)# mayuscula seguida de un punto
    df["Club"]=df["Club"].replace(r'[A-Z]{1}[a-z]{1}[.]',"", regex=True) #mayuscula seguida de minuscula y punto
    df["Club"]=df["Club"].replace(r" de "," ",regex=True)
    df["Club"]=df["Club"].replace(r" United"," Utd")
    df["Club"]=df["Club"].replace(r'[0-9]{1}',"", regex=True)# como minimo un numero
    df["Club"]=df["Club"].str.strip() # Borramos los espacios en blanco por si se ha quedado alguno
    return df

# def concatenar_2(df1,df2):# kargvs , tendriamos que pasar los 10 ficheros
#     """ Función concatena los ficheros  guardadols en sendos dataframes
    
#     Parameters
#     ----------
#     parametro_1 : dataframe
#     Dataframe que deseamos concatenar
#     parametro_2 : dataframe
#     Dataframe que deseamos concatenar
#     .....
#     parametro_10 : dataframe
#     Dataframe que deseamos concatenar

#     Returns
#     -------
#     dataframe
#     Devuelve dos dataframes con los datos concatenados de los 10 df
#     """
#     dataframe1 =pd.concat([df1,df2])
#     data_Fifa=dataframe1
#     return data_Fifa

def cambios_nombre(data_Fifa):
    """ Función limpieza de datos
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos limpiar

    Returns
    -------
    dataframe
    Devuelve dataframe con limpieza de columnas
    """
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"SpVgg Greuther Fürth","Greuther Fürth", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"DArminia Bielefeld","Arminia", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Fortuna Düsseldorf","Düsseldorf", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Tottenham Hotspur","Tottenham", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Toulouse Football Club","Toulouse", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Bayern München","Bayern Munich", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Chievo Verona","Chievo", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Bayer 04 Leverkusen","Leverkusen", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Borussia Dortmund","Dortmund", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Borussia Mönchengladbach","M'Gladbach", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"West Bromwich Albion","West Brom", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Paris","Paris S-G", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Paris S-G Saint-Germain","Paris S-G", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Espanyol Barcelona","Espanyol", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Levante Unión Deportiva","Levante", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Celta","Celta Vigo", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Deportivo La Coruña","La Coruña", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Celta Vigo Vigo","Celta Vigo", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Eintracht Frankfurt","Eint Frankfurt", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Olympique Lyonnais","Lyon", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Olympique Marseille","Marseille", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Liverpool Fútbol Club","Liverpool", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Racing Club Lens","Lens", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Real Betis Balompié","Betis", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Real Betis","Betis", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Werder Bremen II","Werder Bremen", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Freiburg II","Freiburg", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Torino.","Torino", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Udinese Calcio","Udinese", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Vitória","Alavés", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Alaves","Alavés", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Deportivo Alavés","Alavés", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Athletic Club Bilbao","Athletic Club", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"West Ham United","West Ham", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Girondins Bordeaux","Bordeaux", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Wolverhampton Wanderers","Wolves", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Huddersfield Town","Huddersfield", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Leeds Utd","Leeds United", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Nîmes Olympique","Nîmes", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Brighton & Hove Albion","Brighton", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Real Valladolid","Valladolid", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"DijonO","Dijon", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Strasbourg Alsace ","Strasbourg", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Stade Reims","Reims", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"LOLille","Lille", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"En Avant Guingamp","Guingamp", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Stade Malherbe Caen","Caen", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Stade Rennais","Rennes", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"ESTTroyes","Troyes", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"Manchester United","Manchester Utd", regex=True)
    data_Fifa["Club"]=data_Fifa["Club"].replace(r"OGC Nice","Nice", regex=True)
    return data_Fifa

def ligas_pais_ano(df):

    ESP={"Barcelona","Real Madrid","Celta Vigo","Girona","Atlético Madrid",
    "Valencia","Espanyol","Villarreal","Real Sociedad","Getafe","Betis","Alavés",
    "Levante","Athletic Club","Sevilla","La Coruña","Las Palmas","Eibar","Málaga",
    "Leganés","Valladolid","Huesca","Rayo Vallecano","Granada","Osasuna","Mallorca",
    "Cádiz","Elche"}

    ENG={"Liverpool","Tottenham","Manchester City","Leicester City","Manchester Utd",
    "Arsenal","Chelsea","Brighton","West Ham","Burnley","Everton","Crystal Palace",
    "Newcastle Utd","Bournemouth","Stoke City","Watford","Huddersfield","Southampton",
    "Swansea City","West Brom","Wolves","Cardiff City","Fulham","Sheffield Utd",
    "Aston Villa","Norwich City","Leeds United","Brentford"}

    GER={"Bayern Munich","Freiburg","Hoffenheim","Leverkusen","Hannover 96",
    "Dortmund","RB Leipzig","Augsburg","Hertha BSC","Schalke 04","M'Gladbach",
    "Eint Frankfurt","Wolfsburg","Stuttgart","Mainz 05","Werder Bremen",
    "Hamburger SV","Köln","Düsseldorf","Nürnberg","Union Berlin","Paderborn 07",
    "Arminia","Bochum","Greuther Fürth"}


    ITA={"Lazio","Inter","Juventus","Sampdoria","Napoli","Roma","Fiorentina",
    "Torino","Udinese","Chievo","Atalanta","Cagliari","SPAL","Milan","Sassuolo",
    "Bologna","Benevento","Crotone","Genoa","Hellas Verona","Parma","Empoli",
    "Frosinone","Lecce","Brescia","Spezia","Salernitana","Venezia"}

    FRA={"Paris S-G","Marseille","Lyon","Monaco","Nice","Angers","Metz","Amiens",
    "Lille","Bordeaux","Nantes","Dijon","Guingamp","Caen","Rennes","Montpellier",
    "Toulouse","Troyes","Saint-Étienne","Strasbourg","Reims","Nîmes","Brest",
    "Lens","Lorient","Clermont Foot"}

    pais1=pd.DataFrame()
    pais2=pd.DataFrame()
    pais3=pd.DataFrame()
    pais4=pd.DataFrame()
    pais5=pd.DataFrame()

    pais1["Equipo"]=["Barcelona","Liverpool","Tottenham","Bayern Munich","Lazio","Inter",
    "Paris S-G","Real Madrid","Juventus","Marseille","Celta Vigo","Manchester City",
    "Girona","Leicester City","Atlético Madrid","Lyon","Sampdoria","Napoli",
    "Monaco","Nice","Angers","Manchester Utd","Roma","Valencia","Espanyol",
    "Villarreal","Real Sociedad","Freiburg","Metz","Arsenal","Hoffenheim",
    "Leverkusen","Fiorentina","Hannover 96","Dortmund","RB Leipzig","Getafe",
    "Augsburg","Amiens","Lille","Chelsea","Bordeaux","Torino","Nantes",
    "Hertha BSC","Dijon","Udinese","Brighton","Chievo","Schalke 04","Atalanta",
    "Betis","Guingamp","WestHam","Cagliari","SPAL","Caen","Milan","Rennes",
    "Burnley","M'Gladbach","Montpellier","Everton","Alavés","Levante",
    "Crystal Palace","Athletic Club","Sassuolo","Bologna","Sevilla","Eint Frankfurt",
    "Wolfsburg","La Coruña","Las Palmas","Stuttgart","Eibar",
    "Newcastle Utd","Bournemouth","Mainz 05","Toulouse","Troyes","Stoke City",
    "Benevento","Saint-Étienne","Watford","Strasbourg","Huddersfield","Southampton",
    "Crotone","Swansea City","West Brom","Werder Bremen","Genoa","Hamburger SV",
    "Málaga","Leganés","Köln","Hellas Verona"]

    #pais1["Year"] ="2018-01-09"   # Mirar como definir lo del año 

    pais2["Equipo"]=["Manchester City","Liverpool","Paris S-G","Juventus","Bayern Munich",
    "Barcelona","Dortmund","Napoli","Atlético Madrid","Lille","RB Leipzig",
    "Chelsea","Lyon","Tottenham","Arsenal","Atalanta","Inter","Milan","Real Madrid"
    ,"Roma","Saint-Étienne","Manchester Utd","Leverkusen","Torino","M'Gladbach",
    "Wolfsburg","Valencia","Marseille","Eint Frankfurt","Werder Bremen","Sevilla",
    "Getafe","Montpellier","Lazio","Hoffenheim","Wolves","Nice","Reims","Everton",
    "Sampdoria","Nîmes","Espanyol","Athletic Club","Leicester City","Rennes",
    "West Ham","Real Sociedad","Watford","Betis","Alavés","Strasbourg",
    "Crystal Palace","Düsseldorf","Nantes","Hertha BSC","Mainz 05","Eibar","Angers",
    "Leganés","Newcastle Utd","Bournemouth","Villarreal","Levante","Bologna",
    "Sassuolo","Udinese","SPAL","Fiorentina","Bordeaux","Celta Vigo","Cagliari",
    "Valladolid","Parma","Freiburg","Burnley","Southampton","Genoa","Empoli",
    "Amiens","Toulouse","Girona","Schalke 04","Monaco","Brighton","Augsburg","Dijon",
    "Cardiff City","Huesca","Caen","Rayo Vallecano","Stuttgart","Guingamp","Fulham",
    "Frosinone","Hannover 96","Nürnberg","Chievo","Huddersfield"]

    #pais2["Year"] ="2019-01-09"

    pais3["Equipo"]=["Liverpool","Paris S-G","Bayern Munich","Real Madrid","Juventus",
    "Barcelona","Inter","Manchester City","Atalanta","Lazio","Dortmund","Marseille",
    "RB Leipzig","M'Gladbach","Leverkusen","Roma","Atlético Madrid","Sevilla",
    "Rennes","Lille","Manchester Utd","Milan","Chelsea","Leicester City","Napoli",
    "Villarreal","Tottenham","Wolves","Hoffenheim","Arsenal","Real Sociedad",
    "Granada","Reims","Nice","Wolfsburg","Lyon","Montpellier","Monaco","Getafe",
    "Sheffield Utd","Burnley","Freiburg","Strasbourg","Angers","Valencia","Osasuna"
    ,"Southampton","Sassuolo","Athletic Club","Bordeaux","Eint Frankfurt","Nantes",
    "Fiorentina","Parma","Hellas Verona","Levante","Everton","Bologna","Brest",
    "Metz","Hertha BSC","Union Berlin","Cagliari","Udinese","Newcastle Utd",
    "Schalke 04","Crystal Palace","Valladolid","Sampdoria","Eibar","Mainz 05",
    "Betis","Brighton","Dijon","Saint-Étienne","Augsburg","Köln","Torino","West Ham"
    ,"Alavés","Genoa","Celta Vigo","Nîmes","Leganés","Aston Villa","Lecce",
    "Werder Bremen","Bournemouth","Watford","Düsseldorf","Mallorca","Amiens",
    "Espanyol","Brescia","Paderborn 07","Norwich City","SPAL","Toulouse"]

    #pais3["Year"] ="2020-01-09"

    pais4["Equipo"]=["Inter","Bayern Munich","Manchester City","Atlético Madrid",
    "Real Madrid","Lille","Paris S-G","Barcelona","Milan","Atalanta","Juventus",
    "Monaco","Napoli","Sevilla","Lyon","Manchester Utd","RB Leipzig","Dortmund",
    "Liverpool","Wolfsburg","Lazio","Chelsea","Eint Frankfurt","Leicester City",
    "West Ham","Tottenham","Real Sociedad","Roma","Sassuolo","Arsenal","Betis",
    "Marseille","Leeds United","Everton","Villarreal","Leverkusen","Rennes","Lens",
    "Union Berlin","Aston Villa","M'Gladbach","Montpellier","Celta Vigo","Sampdoria",
    "Nice","Stuttgart","Freiburg","Hoffenheim","Metz","Athletic Club",
    "Saint-Étienne","Granada","Hellas Verona","Bordeaux","Newcastle Utd","Wolves",
    "Osasuna","Angers","Cádiz","Crystal Palace","Mainz 05","Valencia","Southampton",
    "Reims","Strasbourg","Genoa","Lorient","Brighton","Levante","Bologna","Brest",
    "Augsburg","Nantes","Fiorentina","Udinese","Hertha BSC","Spezia","Burnley",
    "Arminia","Getafe","Alavés","Cagliari","Torino","Köln","Elche","Nîmes","Werder"
    "Bremen","Huesca","Benevento","Valladolid","Eibar","Fulham","West Brom",
    "Sheffield Utd","Crotone","Dijon","Parma","Schalke 04"]

    #pais4["Year"] ="2021-01-09"

    pais5["Equipo"]=["Manchester City","Liverpool","Real Madrid","Bayern Munich","Paris S-G",
    "Milan","Inter","Napoli","Dortmund","Barcelona","Chelsea","Juventus",
    "Leverkusen","Monaco","Tottenham","Marseille","Atlético Madrid","Arsenal",
    "Sevilla","Rennes","Betis","Lazio","RB Leipzig","Strasbourg","Nice",
    "Union Berlin","Real Sociedad","Lens","Fiorentina","Roma","Freiburg","Atalanta",
    "Lyon","Manchester Utd","Köln","Villarreal","West Ham","Athletic Club","Nantes",
    "Lille","Hellas Verona","Wolves","Torino","Mainz 05","Sassuolo","Hoffenheim",
    "Leicester City","M'Gladbach","Brighton","Brest","Osasuna","Crystal Palace",
    "Celta Vigo","Reims","Eint Frankfurt","Brentford","Wolfsburg","Bochum",
    "Aston Villa","Valencia","Udinese","Newcastle Utd","Montpellier","Bologna",
    "Rayo Vallecano","Augsburg","Espanyol","Southampton","Getafe","Elche","Angers",
    "Empoli","Troyes","Granada","Everton","Cádiz","Stuttgart","Spezia","Mallorca",
    "Clermont Foot","Hertha BSC","Lorient","Leeds United","Burnley","Sampdoria",
    "Levante","Metz","Alavés","Saint-Étienne","Salernitana","Arminia","Cagliari",
    "Genoa","Bordeaux","Venezia","Watford","Norwich City","Greuther Fürth"]

    #pais5["Year"] ="2022-01-09"

    df["Pais"]="Borrar"
    df["Pais"][(df.Club.isin(ESP))&(df.Year=="2018-01-09")]="ESP"
    df["Pais"][(df.Club.isin(FRA))&(df.Year=="2018-01-09")]="FRA"
    df["Pais"][(df.Club.isin(GER))&(df.Year=="2018-01-09")]="GER"
    df["Pais"][(df.Club.isin(ITA))&(df.Year=="2018-01-09")]="ITA"
    df["Pais"][(df.Club.isin(ENG))&(df.Year=="2018-01-09")]="ENG"

    df["Pais"][(df.Club.isin(ESP))&(df.Year=="2019-01-09")]="ESP"
    df["Pais"][(df.Club.isin(FRA))&(df.Year=="2019-01-09")]="FRA"
    df["Pais"][(df.Club.isin(GER))&(df.Year=="2019-01-09")]="GER"
    df["Pais"][(df.Club.isin(ITA))&(df.Year=="2019-01-09")]="ITA"
    df["Pais"][(df.Club.isin(ENG))&(df.Year=="2019-01-09")]="ENG"

    df["Pais"][(df.Club.isin(ESP))&(df.Year=="2020-01-09")]="ESP"
    df["Pais"][(df.Club.isin(FRA))&(df.Year=="2020-01-09")]="FRA"
    df["Pais"][(df.Club.isin(GER))&(df.Year=="2020-01-09")]="GER"
    df["Pais"][(df.Club.isin(ITA))&(df.Year=="2020-01-09")]="ITA"
    df["Pais"][(df.Club.isin(ENG))&(df.Year=="2020-01-09")]="ENG"

    df["Pais"][(df.Club.isin(ESP))&(df.Year=="2021-01-09")]="ESP"
    df["Pais"][(df.Club.isin(FRA))&(df.Year=="2021-01-09")]="FRA"
    df["Pais"][(df.Club.isin(GER))&(df.Year=="2021-01-09")]="GER"
    df["Pais"][(df.Club.isin(ITA))&(df.Year=="2021-01-09")]="ITA"
    df["Pais"][(df.Club.isin(ENG))&(df.Year=="2021-01-09")]="ENG"

    df["Pais"][(df.Club.isin(ESP))&(df.Year=="2022-01-09")]="ESP"
    df["Pais"][(df.Club.isin(FRA))&(df.Year=="2022-01-09")]="FRA"
    df["Pais"][(df.Club.isin(GER))&(df.Year=="2022-01-09")]="GER"
    df["Pais"][(df.Club.isin(ITA))&(df.Year=="2022-01-09")]="ITA"
    df["Pais"][(df.Club.isin(ENG))&(df.Year=="2022-01-09")]="ENG"

    #df = df.drop(df[df['Pais']=="Borrar"].index) 

    return df

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
    data_Fifa = data_Fifa.drop(data_Fifa[data_Fifa['Pais']=="Borrar"].index) 
    data_Fifa.columns = data_Fifa.columns.str.replace(' ', '_') 
    #Valores de las cartas de los jugadores de campo
    data_Fifa['Def_Awareness']= 0
    data_Fifa['Def_Awareness'][(data_Fifa['Marking'].notnull())]=data_Fifa['Marking']
    data_Fifa['Def_Awareness'][(data_Fifa['DefensiveAwareness'].notnull())]=data_Fifa['DefensiveAwareness']
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
    data_Fifa.drop(columns=("DefensiveAwareness"),inplace=True )
    data_Fifa.drop(columns=("Marking"),inplace=True )
    data_Fifa.drop(columns=("Flag"),inplace=True )
    data_Fifa=data_Fifa.drop(["Vision","Composure","Acceleration","SprintSpeed",
    'Finishing','Volleys','ShotPower','LongShots','Positioning','Penalties',
    'Crossing','ShortPassing','Curve','FKAccuracy','LongPassing','Dribbling',
    'BallControl','Balance','Agility','Reactions','Interceptions',
    'StandingTackle','SlidingTackle','HeadingAccuracy','Def_Awareness',
    'Jumping','Stamina','Strength','Aggression'], axis =1)
    #Enviamos a un fichero csv lo que vamos a borrar , como punto de control , por si falta luego algun equipo, asignamos a un df1 temporal lo que no contiene el valor borrar
    # d3=data_Fifa.loc[data_Fifa.Pais=="Borrar"]
    # d3.to_csv("Borrar.csv", sep=',', encoding="utf-32")
    # d1=data_Fifa.loc[data_Fifa.Pais!="Borrar"]
    # data_Fifa=d1    
       
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
    df=df.drop(["ID","Photo","Club_Logo","Real_Face","Position","Name",
    "Nationality","Club","Body_Type","Release_Clause","Joined","Year",
    "Pais","Foot","inc","Contract_Valid_Until","Jersey_Number","ID",
    "Jersey_Number","Height"], axis =1)
    
    return df

def outliers(data_Fifa):
    """ Función limpia y da formato a columna con excepciones
    
    Parameters
    ----------
    parametro_1 : dataframe
    Dataframe que deseamos limpiar/borrar/modificar_columnas

    Returns
    -------
    dataframe1
    Devuelve dataframe con datos modificados
    """
    data_Fifa["Leyenda"]=""
    data_Fifa.loc[data_Fifa['Name'].str.contains(r"[0-9]","",regex=True), 'Leyenda'] = True
    d2=data_Fifa[data_Fifa["Leyenda"] == True].index
    data_Fifa.drop(d2 , inplace=True)
    data_Fifa = data_Fifa.drop('Leyenda', axis=1)
    data_Fifa["Name"]=data_Fifa["Name"].str.strip()
    return data_Fifa

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

def rmsle_cv(model,X_train, y_train):
    n_folds=5
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(X_train.values)
    rmse= np.sqrt(-cross_val_score(model, X_train.values, y_train, scoring="neg_mean_squared_error", cv = kf))
    return(rmse)

def mae_cv(model,X_train, y_train):
    n_folds=5
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(X_train.values)
    mae= np.sqrt(-cross_val_score(model, X_train.values, y_train, scoring="neg_mean_absolute_error", cv = kf))
    return(mae)

def rmse_cv(model,X_train, y_train):
    n_folds=5
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(X_train.values)
    rmse2= np.sqrt(-cross_val_score(model, X_train.values, y_train, scoring="neg_root_mean_squared_error", cv = kf))
    return(rmse2)