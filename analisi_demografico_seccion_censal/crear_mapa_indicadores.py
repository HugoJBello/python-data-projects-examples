import traceback
from osgeo import ogr
import pandas as pd
import os
import sys
sys._enablelegacywindowsfsencoding()
import sys

def add_new_columns_to_layer(layer, column_array):
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


# Extrameos un nuevo layer a partir del nombre del municipio usando el shapefile de toda la comunidad de madrid
def extract_layer_by_nmun(nmun, layer_name, data_source):
    sql = "SELECT * FROM " + layer_name + " WHERE NMUN = '" + nmun + "';COMMIT"
    new_layer_name =  nmun + "_" + layer_name
    result = data_source.ExecuteSQL(sql, dialect='SQLITE')
    layer_new = data_source.CopyLayer(result, new_layer_name)
    result = None
    return layer_new


if __name__ == '__main__':
    shapefile = "data/SECC_CPV_E_20111101_01_R_INE_MADRID.shp"
    data_source = ogr.Open(shapefile, True)  # True allows to edit the shapefile
    layer = data_source.GetLayer()
    #suffix = "indicadores_demograficos_2011_c2011"
    suffix = "datos_padron_edad_20181018"

    route_to_csv_files = "tmp/"

    for fichero in os.listdir(route_to_csv_files):
        nmun = fichero.split("_")[0]
        df_indicadores = pd.read_csv(route_to_csv_files + fichero, sep=";", encoding="utf-8")
        cols = df_indicadores.columns.tolist()[1:]

        layer_suffix = suffix
        layer_new = data_source.CopyLayer(layer, layer_suffix)

        layer_new = extract_layer_by_nmun(nmun, layer_name=layer_suffix, data_source=data_source)
        layer_new = add_new_columns_to_layer(layer_new, cols)
        layer_new = add_data_in_new_columns_to_layer(layer_new, cols, df_indicadores)

