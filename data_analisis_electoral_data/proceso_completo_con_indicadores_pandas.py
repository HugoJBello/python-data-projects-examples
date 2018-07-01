

import os
import pandas as pd



df_f05 = pd.read_csv("recursos_input/F05_1_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")
df_f03 = pd.read_csv("recursos_input/F03_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")
df_f10 = pd.read_csv("recursos_input/F10_MUN_2015.csv",sep=";",error_bad_lines=False, encoding="utf-8")
df_siglas_cand = df_f03[["COD_CAND", "SIGLAS_CAND"]]

df_D3300217_2014 = pd.read_csv("recursos_input/D3300217_2014.csv",sep=",",error_bad_lines=False, encoding="utf-8")
df_D3300217_2014[["CUSEC"]] = df_D3300217_2014[["CUSEC"]].astype(str)

df_indicadores_madrid = pd.read_csv("recursos_input/C2011_ccaa13_Indicadores.csv",sep=",",error_bad_lines=False, encoding="utf-8")


df_indicadores_madrid["%_pob_esp"] = 100 * df_indicadores_madrid["t4_1"]/(df_indicadores_madrid["t4_1"] + df_indicadores_madrid["t4_2"] +df_indicadores_madrid["t4_3"] + df_indicadores_madrid["t4_4"] + df_indicadores_madrid["t4_5"] + df_indicadores_madrid["t4_6"] + df_indicadores_madrid["t4_7"] + df_indicadores_madrid["t4_8"])
df_indicadores_madrid["%_viv_pagada"] = 100 * df_indicadores_madrid["t18_1"]/ (df_indicadores_madrid["t18_1"] + df_indicadores_madrid["t18_2"] +df_indicadores_madrid["t18_3"] + df_indicadores_madrid["t18_4"] + df_indicadores_madrid["t18_5"] + df_indicadores_madrid["t18_6"])
df_indicadores_madrid["%_viv_hipoteca"] = 100 * df_indicadores_madrid["t18_2"]/ (df_indicadores_madrid["t18_1"] + df_indicadores_madrid["t18_2"] +df_indicadores_madrid["t18_3"] + df_indicadores_madrid["t18_4"] + df_indicadores_madrid["t18_5"] + df_indicadores_madrid["t18_6"])
df_indicadores_madrid["%_viv_alquiler"] = 100 * df_indicadores_madrid["t18_4"]/ (df_indicadores_madrid["t18_1"] + df_indicadores_madrid["t18_2"] +df_indicadores_madrid["t18_3"] + df_indicadores_madrid["t18_4"] + df_indicadores_madrid["t18_5"] + df_indicadores_madrid["t18_6"])
df_indicadores_madrid["%_analf"] = 100 * df_indicadores_madrid["t12_1"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])
df_indicadores_madrid["%_no_est"] = 100 * df_indicadores_madrid["t12_2"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])
df_indicadores_madrid["%_est_1_gr"] = 100 * df_indicadores_madrid["t12_3"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])
df_indicadores_madrid["%_est_2_gr"] = 100 * df_indicadores_madrid["t12_4"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])
df_indicadores_madrid["%_est_3_gr"] = 100 * df_indicadores_madrid["t12_5"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])
df_indicadores_madrid["%_est_noinf"] = 100 * df_indicadores_madrid["t12_6"]/(df_indicadores_madrid["t12_1"] + df_indicadores_madrid["t12_2"] +df_indicadores_madrid["t12_3"] + df_indicadores_madrid["t12_4"] + df_indicadores_madrid["t12_5"] + df_indicadores_madrid["t12_6"])
df_indicadores_madrid["CUSEC"] = df_indicadores_madrid["cpro"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_indicadores_madrid["cmun"].astype(str).apply(lambda x: x.rjust(3,"0"))+ df_indicadores_madrid["dist"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_indicadores_madrid["secc"].astype(str).apply(lambda x: x.rjust(3,"0"))

df_indicadores_madrid.to_csv("recursos_input/C2011_ccaa13_Indicadores_tratado.csv", sep=";", index=False)

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

for n_mun in nombres_municipios:
    cod_municipio = df_f05.loc[df_f05['MUNICIPIO'] == n_mun]['COD_MUN'].values.tolist()[0] 			
    cod_ccaa = df_f05.loc[df_f05['MUNICIPIO'] == n_mun]['COD_CCAA'].values.tolist()[0] 
    cod_prov = df_f05.loc[df_f05['MUNICIPIO'] == n_mun]['COD_PROV'].values.tolist()[0] 
    print(cod_ccaa)
    print("----------------------------------------")
    print("filtrando datos para municipio " + n_mun)
    df_municipio = df_f10.loc[(df_f10['COD_MUN'] == cod_municipio) & (df_f10['COD_CCAA']==cod_ccaa) & (df_f10['COD_PROV']==cod_prov)].reset_index()

    print("sumando votos y agrupando por distrito " + n_mun)
    df_resultado = df_municipio.groupby(["TIPO_ELECCION","ANIO","MES", "VUELTA", "COD_CCAA","COD_PROV","COD_MUN","DISTRITO", "SECCION","COD_CAND"],squeeze=False)["VOTOS_CAND"].sum().reset_index()

    print("substituyendo siglas candidatura " + n_mun)
    df_resultado=df_resultado.merge(df_siglas_cand, left_on='COD_CAND', right_on='COD_CAND',left_index=True, how='left')
    del df_resultado["COD_CAND"]
    df_resultado=df_resultado.rename(index=str, columns={"SIGLAS_CAND": "COD_CAND"})

    print("organizando datos " + n_mun)
    df_resultado["CUSEC"] = df_resultado["COD_PROV"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_resultado["COD_MUN"].astype(str).apply(lambda x: x.rjust(3,"0"))+ df_resultado["DISTRITO"].astype(str).apply(lambda x: x.rjust(2,"0")) + df_resultado["SECCION"].astype(str).apply(lambda x: x.rjust(3,"0"))
    df_resultado = pd.pivot_table(df_resultado, values = 'VOTOS_CAND', index=["CUSEC","COD_PROV","DISTRITO", "SECCION"], columns = 'COD_CAND').reset_index()
    df_resultado = df_resultado.rename(index=str, columns={"COD_PROV": "PROV", "DISTRITO": "DIST", "SECCION":"SECC_CEN"})

    print("calculando porcentajes de cada partido para " + n_mun)
    cols_no_partidos=['CUSEC','PROV','DIST','SECC_CEN']
    df_partidos = df_resultado.copy()
    for col in cols_no_partidos: 
        del df_partidos[col]

    suma_partidos = df_partidos.sum(axis=1)
    for col in list(df_resultado):
        if col not in cols_no_partidos:
            nueva_col="%"+col
            df_resultado[nueva_col] = (df_resultado[col]/suma_partidos)*100
            df_resultado[nueva_col]=df_resultado[nueva_col].round(decimals = 3)

    if (n_mun=="Madrid"):
        print("agregando renta per capita en comunidad de madrid")
        df_resultado=df_resultado.merge(df_D3300217_2014[["CUSEC","TRAMO","RENTAMEDIA"]], left_on='CUSEC', right_on='CUSEC',left_index=True, how='left')
        
    if (cod_ccaa==12):
        print("agregando indicadores")
        print(df_indicadores_madrid.columns[-9:].tolist())

        df_resultado=df_resultado.merge(df_indicadores_madrid[df_indicadores_madrid.columns[-9:].tolist()], left_on='CUSEC', right_on='CUSEC',left_index=True, how='left')
        

    print("guardando en fichero de salida")
    dir_salida = "tmp"
    nombre_subfichero_salida = n_mun + "_F10_MUN_2015_denom_cand_agrupado_ruben_pc.csv"
    df_resultado.to_csv(dir_salida + "/" + nombre_subfichero_salida, sep=";", index=False)
