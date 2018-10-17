let fs = require('fs');

export class ConvertCsvRawFilesToJson {
    directory = 'csv_polylines_municipios';
    files = fs.readdirSync(this.directory);
    constructor() { };

    public async convert() {
        await this.files.forEach((fileName: string) => {
            console.log(fileName);
            const csv = fs.readFileSync("./" + this.directory + "/" + fileName)
            let json = this.convertFileTojson(csv, fileName);
            const outputFilename = "./json_polylines_municipios/" + fileName.replace(".csv", ".json");
            fs.writeFileSync(outputFilename, JSON.stringify(json));
        });
    }

    convertFileTojson = (csv: any, fileName: string) => {
        const lines = csv.toString().split("\n");
        const listCusecsJson = []
        for (let line of lines) {
            const cusecJson = this.convertLineToJson(line);
            if (cusecJson) { listCusecsJson.push(cusecJson); }
        }
        return { fileName: fileName.replace(".csv", ".json"), municipioScraped: false, cusecs: listCusecsJson }

    }

    convertLineToJson = (line: string) => {
        let result;
        //index;CUSEC;NMUN;POLYLINE;POLYLINEPREURL;URLENCODED
        if (line.indexOf("NMUN") === -1) {
            let data = line.split(";");
            result = { cusec: data[1], nmun: data[2], urlEncoded: data[5], alreadyScraped: false };
        }
        return result;
    }



}
