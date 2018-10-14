//const polyline = require('@mapbox/polyline');
//var polyline = require( 'google-polyline' )
const encode = require('geojson-polyline').encode

const fs = require('fs')

const directory = 'geoJson_output'
const files = fs.readdirSync(directory);

files.forEach((file)=> {
    const pointsArray2= require("./" + directory + "/" + file);
    //const polylineEncoded = polyline.fromGeoJSON(pointsArray2)
    const polylineEncoded = encode(pointsArray2)["coordinates"];
    console.log(polylineEncoded);
    console.log("\n-----");
    console.log(file);
    console.log("-----");
    console.log(polylineEncoded);
    const polylineEncodedPreURL = "((" + polylineEncoded + "))";
    const urlEncoded =  encodeURIComponent(polylineEncodedPreURL)

    console.log(urlEncoded);
});
