# OBJETIVO: Este script se encarga de transformar los ficheros que nos cede el instituto nacional de estadística.
# Genera por cada .DAT (de datos sin elemento de separación, en crudo) un .CSV con encabezado y los datos separados por ";" en una tabla.

# PROCESO:  buscará el fichero en la ruta que le pongamos en la variable ruta_fichero_sin_procesar. Para saber como tiene que agrupar los datos en 
# columnas deberemos rellenar la lista lista_longitudes_y_descrip con un elemento por cada corte que se deba hacer en cada línea, por ejemplo si los dos
# primeros caracteres son el TIPO_ELECCION pondremos un elemento [2,"TIPO_ELECCION"], si los cuatro siguientes son el año pondremos [4,"ANIO"] después y así

def crear_encabezado(lista_longitudes_y_descrip):
    resultado=""
    for n in range(0,len(lista_longitudes_y_descrip)):
        if (n==0):
            resultado = lista_longitudes_y_descrip[n][1].strip()
        else:
            resultado = resultado +";" +  lista_longitudes_y_descrip[n][1].strip()
    return resultado

def romper_cadenas_datos(datos_txt,lista_longitudes_y_descrip):
    datos_txt_lineas = datos_txt.split("\n")
    csv_salida = [crear_encabezado(lista_longitudes_y_descrip) + "\n"]
    for linea in datos_txt_lineas:
        linea_procesada = ""
        indice = 0
        for n in range(0,len(lista_longitudes_y_descrip)):
            if (n==0):
                linea_procesada = linea[indice:indice + lista_longitudes_y_descrip[n][0]].strip()
            else:
                linea_procesada = linea_procesada +";" +  linea[indice:indice + lista_longitudes_y_descrip[n][0]].strip()
            indice = indice + lista_longitudes_y_descrip[n][0]
        #print(linea_procesada)
        csv_salida = csv_salida + [linea_procesada + "\n"]
    return csv_salida

#----------------------------------------------------------------------------------------------------
# programa principal
if __name__ == "__main__":
    #lista construida con las longitudes de cada bloque y la descripción en orden
    dicc_longitudes_y_descrip_ficheros= {
    "mun_2011/03041505.DAT":[
        [2,"TIPO_ELECCION"],
        [4,"ANIO"],
        [2,"MES"],
        [6,"COD_CAND"],
        [50,"SIGLAS_CAND"],
        [150,"DENOM_CAND"],
        [6,"COD_NPROV"],
        [6,"COD_NAUT"],
        [6,"COD_NNAC"]    
        ],
    "mun_2011/05041505.DAT":[
        [2,"TIPO_ELECCION"],
        [4,"ANIO"],
        [2,"MES"],
        [1,"VUELTA"],
        [2,"COD_CCAA"],
        [2,"COD_PROV"],
        [3,"COD_MUN"],
        [2,"DISTRITO"],
        [100,"MUNICIPIO"],
        [1,"COD_DIST_ELEC"],
        [3,"COD_PART_JUD"],
        [3,"COD_DIP_PROV"],
        [3,"COD_COM"],
        [8,"POBLACION_DER"],
        [5,"N_MESAS"],
        [8,"CENSO"],
        [8,"CENSO_ESCR"],
        [8,"CENSO_CERE"],
        [8,"VOTOS_CERE"],
        [8,"VOTOS_1AVANCE"],
        [8,"VOTOS_2AVANCE"],
        [8,"VOTOS_BLANCO"],
        [8,"VOTOS_NULOS"],
        [8,"VOTOS_CAND"],
        [3,"ESCANIOS"],
        [8,"VOTOS_REFR_SI"],
        [8,"VOTOS_REFR_NO"],
        [1,"DATOS_OFIC"]
    ],
    "mun_2011/06041505.DAT":[
        [2  ,"TIPO_ELECCION"],
        [4  ,"ANIO"],
        [2  ,"MES"],
        [1  ,"VUELTA"],
        [2  ,"COD_PROV"],
        [3  ,"COD_MUN"],
        [2  ,"DIST_ELEC"],
        [6  ,"COD_CAND"],
        [8  ,"VOTOS_CAND"],
        [3  ,"CAND_OBTENIDOS"]
        ],
    "mun_2011/09041505.DAT":[
        [2,"TIPO_ELECCION"],
        [4,"AÑO"],
        [2,"MES"],
        [1,"VUELTA"],
        [2,"COD_CCAA"],
        [2,"COD_PROV"],
        [3,"COD_MUN"],
        [2,"DISTRITO"],
        [4,"SECCION"],
        [1,"MESA"],
        [7,"CENSO"],
        [7,"CENSO_ESCR_CERA"],
        [7,"CENSO_CERE_ESCR"],
        [7,"VOTOS_CERE"],
        [7,"VOTOS_1AVANCE"],
        [7,"VOTOS_2AVANCE"],
        [7,"VOTOS_BLANCO"],
        [7,"VOTOS_NULOS"],
        [7,"VOTOS_CAND"],
        [7,"REFR_SI"],
        [7,"REFR_NO"],
        [1,"DATOS_OFICIALES"]
        ],
    "mun_2011/10041505.DAT": [
        [2,"TIPO_ELECCION"],
        [4,"AÑO"],
        [2,"MES"],
        [1,"VUELTA"],
        [2,"COD_CCAA"],
        [2,"COD_PROV"],
        [3,"COD_MUN"],
        [2,"DISTRITO"],
        [4,"SECCION"],
        [1,"MESA"],
        [6,"COD_CAND"],
        [7,"VOTOS_CAND"]
        ]
    }

    for nombre_fichero in dicc_longitudes_y_descrip_ficheros.keys():
        print("transformando fichero " + nombre_fichero + " en .CSV")
        nombre_fichero_salida = nombre_fichero.split(".DAT")[0] + ".csv"
        lista_longitudes_y_descrip = dicc_longitudes_y_descrip_ficheros[nombre_fichero]
        fichero = open(nombre_fichero,"r")
        datos_txt = fichero.read()
        fichero.close()
        resultado = romper_cadenas_datos(datos_txt, lista_longitudes_y_descrip)
        
        fichero_salida = open(nombre_fichero_salida,"w")
        fichero_salida.writelines(resultado)
        fichero_salida.close()
 