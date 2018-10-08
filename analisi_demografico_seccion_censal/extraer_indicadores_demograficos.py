

import os
import pandas as pd

df_f05 = pd.read_csv("data/F05_1_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")
df_f10 = pd.read_csv("data/F10_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")

df_D3300217_2014 = pd.read_csv("data/D3300217_2014.csv",sep=",",error_bad_lines=False, encoding="utf-8")
df_D3300217_2014[["CUSEC"]] = df_D3300217_2014[["CUSEC"]].astype(str)

df_indicadores_madrid = pd.read_csv("data/C2011_ccaa13_Indicadores.csv",sep=",",error_bad_lines=False, encoding="utf-8")


# Vivienda
df_indicadores_madrid["%_pob_esp"] = (100 * df_indicadores_madrid["t4_1"]/(df_indicadores_madrid["t4_1"] + df_indicadores_madrid["t4_2"] +df_indicadores_madrid["t4_3"] + df_indicadores_madrid["t4_4"] + df_indicadores_madrid["t4_5"] + df_indicadores_madrid["t4_6"] + df_indicadores_madrid["t4_7"] + df_indicadores_madrid["t4_8"])).round(decimals = 3)
df_indicadores_madrid["%_viv_pag"] = (100 * df_indicadores_madrid["t18_1"]/ (df_indicadores_madrid["t18_1"] + df_indicadores_madrid["t18_2"] +df_indicadores_madrid["t18_3"] + df_indicadores_madrid["t18_4"] + df_indicadores_madrid["t18_5"] + df_indicadores_madrid["t18_6"])).round(decimals = 3)
df_indicadores_madrid["%_viv_hip"] = (100 * df_indicadores_madrid["t18_2"]/ (df_indicadores_madrid["t18_1"] + df_indicadores_madrid["t18_2"] +df_indicadores_madrid["t18_3"] + df_indicadores_madrid["t18_4"] + df_indicadores_madrid["t18_5"] + df_indicadores_madrid["t18_6"])).round(decimals = 3)
df_indicadores_madrid["%_viv_alq"] = (100 * df_indicadores_madrid["t18_4"]/ (df_indicadores_madrid["t18_1"] + df_indicadores_madrid["t18_2"] +df_indicadores_madrid["t18_3"] + df_indicadores_madrid["t18_4"] + df_indicadores_madrid["t18_5"] + df_indicadores_madrid["t18_6"])).round(decimals = 3)

# Estudios
df_indicadores_madrid["%_analf"] = (100 * df_indicadores_madrid["t12_1"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])).round(decimals = 3)
df_indicadores_madrid["%_no_est"] = (100 * df_indicadores_madrid["t12_2"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])).round(decimals = 3)
df_indicadores_madrid["%_est_1_g"] = (100 * df_indicadores_madrid["t12_3"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])).round(decimals = 3)
df_indicadores_madrid["%_est_2_g"] = (100 * df_indicadores_madrid["t12_4"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])).round(decimals = 3)
df_indicadores_madrid["%_est_3_g"] = (100 * df_indicadores_madrid["t12_5"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])).round(decimals = 3)
df_indicadores_madrid["%_est_noi"] = (100 * df_indicadores_madrid["t12_6"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])).round(decimals = 3)

# Edad. Hombres de menos de 16, hombres de entre 16 y 64, hombres mayores de 65
df_indicadores_madrid["%_h_16"] = (100 * df_indicadores_madrid["t7_1"]/(df_indicadores_madrid["t2_1"] )).round(decimals = 3)
df_indicadores_madrid["%_h_med"] = (100 * df_indicadores_madrid["t7_2"]/(df_indicadores_madrid["t2_1"] )).round(decimals = 3)
df_indicadores_madrid["%_h_64"] = (100 * df_indicadores_madrid["t7_3"]/(df_indicadores_madrid["t2_1"] )).round(decimals = 3)

# Edad. Mujeres de menos de 16,mujeres de entre 16 y 64, mujeres mayores de 65
df_indicadores_madrid["%_m_16"] = (100 * df_indicadores_madrid["t7_4"]/(df_indicadores_madrid["t2_2"] )).round(decimals = 3)
df_indicadores_madrid["%_m_med"] = (100 * df_indicadores_madrid["t7_5"]/(df_indicadores_madrid["t2_2"] )).round(decimals = 3)
df_indicadores_madrid["%_m_64"] = (100 * df_indicadores_madrid["t7_6"]/(df_indicadores_madrid["t2_2"] )).round(decimals = 3)

# sexo. Hombres y mujeres
df_indicadores_madrid["%_hombr"] = (100 * df_indicadores_madrid["t2_1"]/(df_indicadores_madrid["t1_1"] )).round(decimals = 3)
df_indicadores_madrid["%_mujer"] = (100 * df_indicadores_madrid["t2_2"]/(df_indicadores_madrid["t1_1"] )).round(decimals = 3)

df_indicadores_madrid["CUSEC"] = (df_indicadores_madrid["cpro"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_indicadores_madrid["cmun"].astype(str).apply(lambda x: x.rjust(3,"0"))+ df_indicadores_madrid["dist"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_indicadores_madrid["secc"].astype(str).apply(lambda x: x.rjust(3,"0")))

df_indicadores_madrid.to_csv("data/C2011_ccaa13_Indicadores_tratado.csv", sep=";", index=False)

print(df_indicadores_madrid)
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


    if (n_mun=="Madrid"):
        print("agregando renta per capita en municipiuo madrid")
        df_municipio=df_municipio.merge(df_D3300217_2014[["CUSEC","TRAMO","RENTAMED"]], left_on='CUSEC', right_on='CUSEC',left_index=True, how='left')
        
    if (cod_ccaa==12):
        print("agregando indicadores")
        df_municipio=df_municipio.merge(df_indicadores_madrid[df_indicadores_madrid.columns[-19:].tolist()], left_on='CUSEC', right_on='CUSEC',left_index=True, how='left')
        

    print("guardando en fichero de salida")
    dir_salida = "tmp"
    nombre_subfichero_salida = n_mun + "_indicadores_demograficos_2011_c2011_ccaa12.csv"
    df_municipio.to_csv(dir_salida + "/" + nombre_subfichero_salida, sep=";", index=False, encoding="utf-8")
