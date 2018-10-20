

import os
import pandas as pd

df_f05 = pd.read_csv("data/F05_1_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")
df_f10 = pd.read_csv("data/F10_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")

df_edad_padron = pd.read_csv("data/output_padron_181018.csv", sep=";", error_bad_lines=False, encoding="utf-8")

df_edad_padron["CUSEC"]= df_edad_padron["CUSEC"].apply(str)

print(df_edad_padron)
nombres_municipios = ["Madrid", "Móstoles", "Alcalá de Henares",
							"Fuenlabrada", "Leganés", "Getafe",
							"Alcorcón", "Torrejón de Ardoz", "Parla", "Alcobendas",
							"Las Rozas de Madrid", "San Sebastián de los Reyes",
							"Pozuelo de Alarcón", "Coslada", "Rivas-Vaciamadrid",
							"Valdemoro", "Majadahonda", "Collado Villalba", "Aranjuez",
							"Arganda del Rey", "Boadilla del Monte", "Pinto", "Colmenar Viejo",
							"Tres Cantos", "San Fernando de Henares", "Galapagar", "Arroyomolinos",
							"Villaviciosa de Odón", "Navalcarnero", "Ciempozuelos", "Torrelodones",
							"Paracuellos de Jarama", "Mejorada del Campo", "Algete"]

# nombres_municipios =["Alcalá de Henares"]

for n_mun in nombres_municipios:
    cod_municipio = df_f05.loc[df_f05['MUNICIPIO'] == n_mun]['COD_MUN'].values.tolist()[0] 			
    cod_ccaa = df_f05.loc[df_f05['MUNICIPIO'] == n_mun]['COD_CCAA'].values.tolist()[0] 
    cod_prov = df_f05.loc[df_f05['MUNICIPIO'] == n_mun]['COD_PROV'].values.tolist()[0] 
    print(cod_ccaa)
    print("----------------------------------------")
    print("filtrando datos para municipio " + n_mun)
    df_municipio = df_f10.loc[(df_f10['COD_MUN'] == cod_municipio) & (df_f10['COD_CCAA']==cod_ccaa) & (df_f10['COD_PROV']==cod_prov)].reset_index()
    print("organizando datos " + n_mun)
    df_municipio["CUSEC"] = df_municipio["COD_PROV"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_municipio["COD_MUN"].astype(str)\
        .apply(lambda x: x.rjust(3,"0"))+ df_municipio["DISTRITO"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_municipio["SECCION"].astype(str).apply(lambda x: x.rjust(3,"0"))
    df_municipio = df_municipio.rename(index=str, columns={"COD_PROV": "PROV", "DISTRITO": "DIST", "SECCION":"SECC_CEN"}).reset_index()

    df_municipio = df_municipio.drop_duplicates(subset='CUSEC', keep="first")

    cols_a_dejar = ["CUSEC"]
    cols_a_borrar = list(filter(lambda x: x not in cols_a_dejar, list(df_municipio)))

    df_municipio = df_municipio.drop(columns=cols_a_borrar)

    if (cod_ccaa==12):
        print("agregando datos edad del padrón")
        df_municipio=df_municipio.merge(df_edad_padron, left_on='CUSEC', right_on='CUSEC', left_index=True, how='left')
        

    print("guardando en fichero de salida")
    dir_salida = "tmp"
    sufijo = "_datos_padron_edad_20181018.csv"
    nombre_subfichero_salida = n_mun + sufijo
    df_municipio.to_csv(dir_salida + "/" + nombre_subfichero_salida, sep=";", index=False, encoding="utf-8")
