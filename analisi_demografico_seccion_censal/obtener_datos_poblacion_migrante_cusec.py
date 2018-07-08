

import os
import pandas as pd


df_f05 = pd.read_csv("data/F05_1_GEN_2016.csv",sep=";",error_bad_lines=False, encoding="utf-8")
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

df_nacionalidad_2017["%EXTRANGEROS_2017"] = df_nacionalidad_2017["Total Extranjeros"]/df_nacionalidad_2017["Total Población"]*100
df_nacionalidad_2016["%EXTRANGEROS_2016"] = df_nacionalidad_2016["Total Extranjeros"]/df_nacionalidad_2016["Total Población"]*100
df_nacionalidad_2015["%EXTRANGEROS_2015"] = df_nacionalidad_2015["Total Extranjeros"]/df_nacionalidad_2015["Total Población"]*100
df_nacionalidad_2011["%EXTRANGEROS_2011"] = df_nacionalidad_2011["Total Extranjeros"]/df_nacionalidad_2011["Total Población"]*100

df_resultado = df_resultado.merge(df_nacionalidad_2011[["CUSEC","%EXTRANGEROS_2011"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left')
print(df_resultado)
df_resultado = df_resultado.merge(df_nacionalidad_2015[["CUSEC","%EXTRANGEROS_2015"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left')
print(df_resultado)
df_resultado = df_resultado.merge(df_nacionalidad_2016[["CUSEC","%EXTRANGEROS_2016"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left').reset_index()
df_resultado = df_resultado.merge(df_nacionalidad_2017[["CUSEC","%EXTRANGEROS_2017"]], left_on='CUSEC', right_on='CUSEC', left_index=False, how='left').reset_index()
df_resultado.xs('CUSEC', axis=1, drop_level=True)


print("guardando en fichero de salida")
dir_salida = "tmp"
nombre_subfichero_salida = "datos_poblac_migrante_2017-2016-2015-2011.csv"
df_resultado.to_csv(nombre_subfichero_salida, sep=";", index=False)


print(df_resultado)