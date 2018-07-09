

import os
import pandas as pd


df_nacionalidad_2017 = pd.read_csv("data/pob_pais_nacionalidad_2017.csv",sep=",",skiprows=5 , encoding="utf-8")
df_nacionalidad_2016 = pd.read_csv("data/pob_pais_nacionalidad_2016.csv",sep=",",skiprows=5, encoding="utf-8")
df_nacionalidad_2015 = pd.read_csv("data/pob_pais_nacionalidad_2015.csv",sep=",",skiprows=5, encoding="utf-8")
df_nacionalidad_2011 = pd.read_csv("data/pob_pais_nacionalidad_2011.csv",sep=",",skiprows=5, encoding="utf-8")

df_nacimiento_2017 = pd.read_csv("data/pob_pais_nacimiento_2017.csv",sep=",",skiprows=5, encoding="utf-8")
df_nacimiento_2016 = pd.read_csv("data/pob_pais_nacimiento_2016.csv",sep=",",skiprows=5, encoding="utf-8")
df_nacimiento_2015 = pd.read_csv("data/pob_pais_nacimiento_2015.csv",sep=",",skiprows=5, encoding="utf-8")
df_nacimiento_2011 = pd.read_csv("data/pob_pais_nacimiento_2011.csv",sep=",",skiprows=5, encoding="utf-8")

print(df_nacionalidad_2017)

df_resultado = df_nacionalidad_2017.copy()[["CUSEC"]]

df_nacionalidad_2017["%EXTR_17"] = df_nacionalidad_2017["Total Extranjeros"]/df_nacionalidad_2017["Total Población"]*100
df_nacionalidad_2016["%EXTR_16"] = df_nacionalidad_2016["Total Extranjeros"]/df_nacionalidad_2016["Total Población"]*100
df_nacionalidad_2015["%EXTR_15"] = df_nacionalidad_2015["Total Extranjeros"]/df_nacionalidad_2015["Total Población"]*100
df_nacionalidad_2011["%EXTR_11"] = df_nacionalidad_2011["Total Extranjeros"]/df_nacionalidad_2011["Total Población"]*100

df_resultado = df_resultado.merge(df_nacionalidad_2011[["CUSEC","%EXTR_11","Total Población"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left').round(decimals = 2)
df_resultado=df_resultado.rename(index=str, columns={"Total Población": "POBL_11"})

df_resultado = df_resultado.merge(df_nacionalidad_2015[["CUSEC","%EXTR_15","Total Población"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left').round(decimals = 2)
df_resultado=df_resultado.rename(index=str, columns={"Total Población": "POBL_15"})

df_resultado = df_resultado.merge(df_nacionalidad_2016[["CUSEC","%EXTR_16","Total Población"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left').round(decimals = 2)
df_resultado=df_resultado.rename(index=str, columns={"Total Población": "POBL_16"})

df_resultado = df_resultado.merge(df_nacionalidad_2017[["CUSEC","%EXTR_17","Total Población"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left').round(decimals = 2)
df_resultado=df_resultado.rename(index=str, columns={"Total Población": "POBL_17"})

cols_ordenadas = ["CUSEC","%EXTR_11","%EXTR_15","%EXTR_16","%EXTR_17","POBL_11","POBL_15","POBL_16","POBL_17"]
df_resultado=df_resultado[cols_ordenadas]


#del df_resultado["level_0"]
#del df_resultado["index"]

print(df_resultado)

print("guardando en fichero de salida")
dir_salida = "tmp"
nombre_subfichero_salida = "datos_poblac_migrante_2017-2016-2015-2011.csv"
df_resultado.to_csv(nombre_subfichero_salida, sep=";", index=False)


print(df_resultado)