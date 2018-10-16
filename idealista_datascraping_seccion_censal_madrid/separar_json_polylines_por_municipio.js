const directory = 'csv_polylines_municipios'
let fs = require('fs');

const files = fs.readdirSync(directory);
console.log(files);
convertFileTojson = (csv, fileName) => {
    const lines = csv.toString().split("\n");
    const listCusecsJson = []
    for (line of lines) {
        cusecJson = convertLineToJson(line);
        if (cusecJson) { listCusecsJson.push(cusecJson); }
    }
    return { fileName: fileName.replace(".csv", ".json"), municipioScraped: false, cusecs: listCusecsJson }

}

convertLineToJson = (line) => {
    let result;
    //index;CUSEC;NMUN;POLYLINE;POLYLINEPREURL;URLENCODED
    if (line.indexOf("NMUN") === -1) {
        let data = line.split(";");
        result = { cusec: data[1], nmun: data[2], urlEncoded: data[5], alreadyScraped: false };
    }
    return result;
}



files.forEach((fileName) => {
    console.log(fileName);
    const csv = fs.readFileSync("./" + directory + "/" + fileName)
    json = convertFileTojson(csv, fileName);
    const outputFilename = "./json_polylines_municipios/" + fileName.replace(".csv", ".json");
    fs.writeFileSync(outputFilename, JSON.stringify(json));
});
