from selenium import webdriver
import time
import random
polylines_csv_file = "encoded_polylines_madrid.csv"
nmuns = ["Alcorcón"]

def obtain_urls_from_csv():
    return ["https://www.idealista.com/en/areas/venta-viviendas/?shape=((ywjvFjhbSRa%40LTnOdYtIzO%60Tf_%40p%5D~n%40bK%60RjPdZf%5Czl%40tCfFrFxJtBvDhOfXnBlE~%40dBjAxBnC%7CEnA~BjElHpCbFjGzKfDhGPZfAlBjBdD~BdEl%40pAhAnB%60GnKdAlBnItOx%40~A%5Er%40b%40%7C%40q%40r%40gAnAq%40%7C%40QVs%40pA_%40r%40Z%60%40_AnBcAlBk%40hAcAiAkAgA%5BuAo%40wCmCiLqCeLqCsIeBsFKQGMgAmCc%40iA%7DBiFGMqDoHKQ_AiBq%40kA_BgCsAaBwFoIuDuFeAuAmMoPuGaJcF%7BGy%40gAuJgMgFwGe%5D_e%40wbBizBcImKLONQaByBGIW%5D_CcDRYPY%40m%40d%40Cn%40I%60%40ILCr%40Ql%40Qn%40S%5CQ%5EUXW%5E%5D~EkGdDgEx%40cAiDiPnA%7DA))"]

def main():
    #driver = webdriver.Edge()
    #driver = webdriver.Chrome()
    driver = webdriver.Firefox()

    urls = obtain_urls_from_csv()

if __name__ == '__main__':
    main()