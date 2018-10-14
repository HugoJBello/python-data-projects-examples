from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import pandas as pd
from datetime import datetime
import sys
sys.getfilesystemencoding()
sys._enablelegacywindowsfsencoding()

polylines_csv_file = "encoded_polylines_madrid.csv"
nmuns = ["Alcorcón"]

fecha_ejec = str(datetime.now())
def obtain_csv_files():
    return ["csv_polylines_municipios/test_polylines_2011_ccaa12.csv"]

def obtener_url_venta_csv(row):
    polyline_encoded = row["URLENCODED"]
    inicio_url = "https://www.idealista.com/en/areas/venta-viviendas/?shape="
    return inicio_url + polyline_encoded

def obtener_url_alquiler_csv(row):
    polyline_encoded = row["URLENCODED"]
    inicio_url = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape="
    return inicio_url + polyline_encoded

def main():
    #driver = webdriver.Edge()
    #driver = webdriver.Chrome()
    #driver = webdriver.Ie()
    driver = webdriver.Firefox()
    for csv_file in obtain_csv_files():
        print(csv_file)
        df_polylines_municipio = pd.read_csv(csv_file, sep=";", error_bad_lines=False, encoding="utf-8")
        df_polylines_municipio["P_VENTA"] = ""
        df_polylines_municipio["V_VENTA"] = ""
        df_polylines_municipio["P_ALQL"] = ""
        df_polylines_municipio["V_ALQL"] = ""
        df_polylines_municipio["FECHA"] = ""

        for index, row in df_polylines_municipio.iterrows():
            url_venta = obtener_url_venta_csv(row)
            print("obteniendo datos de venta " + url_venta)
            try:
                datos = obtener_precio_y_anuncios(driver,url_venta)
                cusec = row["CUSEC"]
                df_polylines_municipio.loc[index,"P_VENTA"]= datos["average_prize"]
                df_polylines_municipio.loc[index,"V_VENTA"]= datos["number_of_items"]
                df_polylines_municipio.loc[index,"FECHA"]= fecha_ejec

            except:
                print("error")
                df_polylines_municipio.loc[index, "P_VENTA"] = 0
                df_polylines_municipio.loc[index, "V_VENTA"] = 0
                df_polylines_municipio.loc[index,"FECHA"]= fecha_ejec

                saltar_captcha(driver)

            url_alquiler = obtener_url_alquiler_csv(row)
            print("obteniendo datos de alquiler " + url_alquiler)
            try:
                datos = obtener_precio_y_anuncios(driver,url_alquiler)
                cusec = row["CUSEC"]
                df_polylines_municipio.loc[index,"P_ALQL"]= datos["average_prize"]
                df_polylines_municipio.loc[index,"V_ALQL"]= datos["number_of_items"]
                df_polylines_municipio.loc[index,"FECHA"]= fecha_ejec
            except:
                print("error")
                df_polylines_municipio.loc[index, "P_ALQL"] = 0
                df_polylines_municipio.loc[index, "V_ALQL"] = 0
                df_polylines_municipio.loc[index,"FECHA"]= fecha_ejec
                saltar_captcha(driver)

        dir_salida = "tmp"
        nombre_subfichero_salida = csv_file.replace(".csv","").split("/")[1] + "_scraped.csv"
        print("guardando " + nombre_subfichero_salida)
        df_polylines_municipio = df_polylines_municipio[["CUSEC","NMUN","P_VENTA","V_VENTA","P_ALQL","V_ALQL","FECHA"]]
        df_polylines_municipio.to_csv(dir_salida +"/" + nombre_subfichero_salida, sep=";", index=False)


def obtener_precio_y_anuncios(driver,url):
    saltar_captcha(driver)
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

def saltar_captcha(driver):
    try:
        capcha_box = driver.find_element_by_xpath("//p[contains(text(),'Vaya! parece que estamos recibiendo muchas peticiones tuyas')]")
        time.sleep(random.uniform(0.5, 0.9))
        print("capcha ha saltado")
        time.sleep(random.uniform(2.5, 2.9))
        raise Exception;
    except NoSuchElementException:
        pass





if __name__ == '__main__':
    main()