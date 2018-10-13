from osgeo import ogr
from osgeo import osr
src = osr.SpatialReference()
src.SetWellKnownGeogCS( "WGS84" );
shapefile = "data/SECC_CPV_E_20111101_01_R_INE_MADRID_cs_epsg_2.shp"
data_source = ogr.Open(shapefile,False)  # True allows to edit the shapefile
layer = data_source.GetLayer()

feature = layer.GetNextFeature()
while feature:
    geom = feature.GetGeometryRef()
    print(geom.Centroid().ExportToWkt())
    print(geom.Boundary().ExportToJson())
    print(geom.Boundary().ExportToWkt())
    feature = layer.GetNextFeature()