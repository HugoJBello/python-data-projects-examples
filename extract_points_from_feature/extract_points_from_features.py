from osgeo import ogr
from pypolyline.util import encode_coordinates
import polyline

import json
import urllib.parse
shapefile = "data/SECC_CPV_E_20111101_01_R_INE_MADRID_cs_epsg.shp"
data_source = ogr.Open(shapefile,False)  # True allows to edit the shapefile
layer = data_source.GetLayer()

feature = layer.GetNextFeature()
while feature:
    geom = feature.GetGeometryRef()
    cusec =feature.GetField("CUSEC")
    nmun =feature.GetField("NMUN")
    polyline_dic = geom.Boundary().ExportToJson()
    filename =  "geoJson_output/" + cusec +"__"+ nmun +"__2011_ine_geojson.json"
    text_file = open(filename, "w")
    text_file.write(polyline_dic)
    text_file.close()
    print(polyline_dic)
    #encoded_polyline = polyline.encode(polyline_dic["coordinates"],5)
    #print(encoded_polyline)
    #url_encoded_polyline = "((" + encoded_polyline + "))"
    #print(url_encoded_polyline)
    #print(urllib.parse.quote_plus(url_encoded_polyline))
    feature = layer.GetNextFeature()