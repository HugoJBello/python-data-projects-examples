import traceback
from osgeo import ogr
import pandas as pd

def add_new_columns_to_layer( layer, column_array):
    for col in column_array:
        if ("%" in col):
            new_field = ogr.FieldDefn(col, ogr.OFTReal)
            new_field.SetWidth(6)
            new_field.SetPrecision(3)
        else:
            if ("CUSEC" in col):
                new_field = ogr.FieldDefn(col, ogr.OFTString)
            else:
                new_field = ogr.FieldDefn(col, ogr.OFTInteger)
        if (layer): layer.CreateField(new_field)
    return layer

    # Rellenamos las columnas nuevas con los datos de los votos


def add_data_in_new_columns_to_layer(layer, column_array, df_partidos):
    if (layer):
        feature = layer.GetNextFeature()
        while feature:
            for col in column_array:
                cusec = feature.GetField("CUSEC")
                try:
                    value = df_partidos.loc[df_partidos["CUSEC"].isin([cusec])].iloc[0][col]
                    col_short = col[0:9]
                    if (not "%" in col_short):
                        feature.SetField(col_short, str(value))
                    else:
                        feature.SetField(col_short, value)
                    layer.SetFeature(feature)
                except:
                    traceback.print_exc()
            feature = layer.GetNextFeature()
    return layer

if __name__ == '__main__':
    shapefile = "data/SECC_CPV_E_20111101_01_R_INE_MADRID.shp"
    data_source = ogr.Open(shapefile,True)  # True allows to edit the shapefile
    layer = data_source.GetLayer()

    df_migrantes = pd.read_csv("datos_poblac_migrante_2017-2016-2015-2011.csv",sep=";",encoding="utf-8")
    cols = df_migrantes.columns.tolist()[1:]

    layer_new =data_source.CopyLayer(layer, "datos_migrantes")
    layer_new = add_new_columns_to_layer(layer_new,cols)
    layer_new = add_data_in_new_columns_to_layer(layer_new,cols,df_migrantes)
    print(cols)

