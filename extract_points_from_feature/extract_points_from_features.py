from osgeo import ogr

shapefile = "data/Alcorcón_indicadores_demograficos_2011_c2011.shp"
data_source = ogr.Open(shapefile,False)  # True allows to edit the shapefile
layer = data_source.GetLayer()

feature = layer.GetNextFeature()
while feature:
    geom = feature.GetGeometryRef()
    print(geom.Centroid().ExportToWkt())
    print(geom.Boundary().ExportToJson())
    print(geom.Boundary().ExportToWkt())
    feature = layer.GetNextFeature()