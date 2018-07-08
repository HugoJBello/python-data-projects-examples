
import pandas as pd

if __name__ == "__main__":
    df=pd.read_fwf("microdatos_poblacion_ine_2017_madrid/madrid_2017__test.txt", widths=[2, 3, 1, 2, 3, 3, 3, 2, 2], names=["CPRO","CMUN","SEXO","CPRON", "CMUNN", "NACI", "EDAD", "TAMU", "TAMUN"]  )
    print(df)