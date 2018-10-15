from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import time
import random
import pandas as pd
from datetime import datetime
import sys, os
from random import shuffle

#pip 3 install dnspython
#pip 3 install pandas

sys.getfilesystemencoding()
sys._enablelegacywindowsfsencoding()

#client = MongoClient('mongodb://freshkore:1234@ds231460.mlab.com:31460/real-state-db')
client = MongoClient('mongodb+srv://fresh:1234@cluster0-ojz1y.mongodb.net/real-state-db?retryWrites=true')
db =client['real-state-db']
cusecs_idealista_collection = db.cusecs_idealista
errores_cusecs_idealista_collection = db.errores_cusecs_idealista
guardado_en_mongo = False

fecha_ejec = str(datetime.now())
csv_dir = "csv_polylines_municipios"

def main():
    driver = webdriver.Edge()
    #driver = webdriver.Chrome()
    #driver = webdriver.Ie()
    #driver = webdriver.Firefox()
    for csv_file in obtain_csv_files():
        print(csv_file)
        df_polylines_municipio = pd.read_csv(csv_dir+"/"+csv_file, sep=";", error_bad_lines=False, encoding="utf-8")
        df_polylines_municipio["P_VENTA"] = 0
        df_polylines_municipio["N_VENTA"] = 0
        df_polylines_municipio["P_ALQL"] = 0
        df_polylines_municipio["N_ALQL"] = 0
        df_polylines_municipio["FECHA"] = fecha_ejec
        df_polylines_municipio.reset_index()

        for index, row in df_polylines_municipio.iterrows():
            url_venta = obtener_url_venta_csv(row)
            data = dict()
            data["fecha"] = fecha_ejec
            data["p_venta"] = 0
            data["n_venta"] = 0
            data["p_alql"] = 0
            data["n_alql"] = 0
            data["cusec"] = int(df_polylines_municipio.loc[index,"CUSEC"])
            data["nmun"] = df_polylines_municipio.loc[index,"NMUN"]
            data["_id"] = str(df_polylines_municipio.loc[index,"CUSEC"]) + "--" + fecha_ejec.replace(":","__").replace(" ","_")
            print("obteniendo datos de venta para municipio " + data["nmun"] +" en url:\n" + url_venta)
            try:
                cusec = row["CUSEC"]
                datos_scraping = obtener_precio_y_anuncios(driver,url_venta)
                df_polylines_municipio.loc[index,"P_VENTA"]= datos_scraping["average_prize"]
                df_polylines_municipio.loc[index,"N_VENTA"]= datos_scraping["number_of_items"]
                df_polylines_municipio.loc[index,"FECHA"]= fecha_ejec
                data["p_venta"] = datos_scraping["average_prize"]
                data["n_venta"] = datos_scraping["number_of_items"]

            except:
                print("error")
                saltar_captcha(driver,cusec)

            url_alquiler = obtener_url_alquiler_csv(row)
            print("obteniendo datos de alquiler para municipio " + data["nmun"] +" en url:\n" + url_alquiler)
            cusec = row["CUSEC"]

            try:
                datos_scraping = obtener_precio_y_anuncios(driver,url_alquiler)
                df_polylines_municipio.loc[index,"P_ALQL"]= datos_scraping["average_prize"]
                df_polylines_municipio.loc[index,"N_ALQL"]= datos_scraping["number_of_items"]
                df_polylines_municipio.loc[index,"FECHA"]= fecha_ejec
                data["p_alql"] = datos_scraping["average_prize"]
                data["n_alql"] = datos_scraping["number_of_items"]

            except:
                print("error")
                saltar_captcha(driver,cusec)

            if (guardado_en_mongo): guardar_en_mongodb(data)

        dir_salida = "tmp"
        nombre_subfichero_salida = csv_file.replace(".csv","") + "_scraped.csv"
        print("guardando " + nombre_subfichero_salida)
        df_polylines_municipio = df_polylines_municipio[["CUSEC","NMUN","P_VENTA","N_VENTA","P_ALQL","N_ALQL","FECHA"]]
        df_polylines_municipio.to_csv(dir_salida +"/" + nombre_subfichero_salida, sep=";", index=False)

def obtain_csv_files():
    #return ["csv_polylines_municipios/test_polylines_2011_ccaa12.csv"]
    files = os.listdir(csv_dir)
    shuffle(files)
    return files

def obtener_url_venta_csv(row):
    polyline_encoded = row["URLENCODED"]
    inicio_url = "https://www.idealista.com/en/areas/venta-viviendas/?shape="
    return inicio_url + polyline_encoded

def obtener_url_alquiler_csv(row):
    polyline_encoded = row["URLENCODED"]
    inicio_url = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape="
    return inicio_url + polyline_encoded

def obtener_precio_y_anuncios(driver,url):
    resultado = {}
    driver.get(url)
    driver.set_page_load_timeout(20)
    item_info_container = driver.find_elements_by_class_name("item-info-container")

    random_int = 8573 + random.randint(-3, 3)
    driver.execute_script("window.scrollTo(0, " + str(random_int) + ");")
    time.sleep(random.uniform(0.5, 1.9))
    average_prize = driver.find_elements_by_class_name("items-average-price")[0].text.replace("Average price:","").replace("eur/m²","").replace(",", "").strip()
    print(average_prize)
    number_of_items = driver.find_elements_by_class_name("h1-simulated")[0].text.split(" ")[0].strip()
    print(number_of_items)

    resultado["average_prize"] = average_prize
    resultado["number_of_items"] = number_of_items
    return resultado

def saltar_captcha(driver,cusec):
    try:
        capcha_box = driver.find_element_by_xpath("//p[contains(text(),'Vaya! parece que estamos recibiendo muchas peticiones tuyas')]")
        time.sleep(random.uniform(0.5, 0.9))
        print("capcha ha saltado")
        time.sleep(random.uniform(2.5, 2.9))
        if(guardar_en_mongo): registrar_error(cusec)
        raise Exception
    except NoSuchElementException:
        pass

def guardar_en_mongodb(data):
    cusecs_idealista_collection.save(data)

def registrar_error(cusec):
    txt = "error de captcha al hacer scraping"
    error = dict()
    error["texto"] = txt
    error["cusec"] = int(cusec)
    error["fecha"] = fecha_ejec
    error["_id"] = str(cusec) +"--"+ fecha_ejec.replace(":","__").replace(" ","_")
    errores_cusecs_idealista_collection.save(error)


if __name__ == '__main__':
    main()