# https://gis.stackexchange.com/questions/41465/generating-geojson-with-python
import fiona
import json

features = []
crs = None
with fiona.collection("data/Alcorcón_indicadores_demograficos_2011_c2011.shp", "r") as source:
    print(source.crs)
    for feat in source:
        #feat['properties'].update(...) # with your attributes
        features.append(feat)
    crs = " ".join("+%s=%s" % (k,v) for k,v in source.crs.items())

my_layer = {
    "type": "FeatureCollection",
    "features": features,
    "crs": {
        "type": "link",
        "properties": {"href": "my_layer.crs", "type": "proj4"} }}

with open("my_layer.json", "w") as f:
    f.write(json.dumps(my_layer))
with open("my_layer.crs", "w") as f:
    f.write(crs)