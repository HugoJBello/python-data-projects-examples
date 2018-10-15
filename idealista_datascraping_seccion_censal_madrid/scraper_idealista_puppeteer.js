const url = "https://www.idealista.com/en/areas/venta-viviendas/?shape=((adhuFn~iVNb%40Pp%40%5EnAJd%40Nn%40%5BRYNYN%5EtA_Af%40g%40P%5BJBLTtAJj%40ZnBq%40Oo%40MOISKC%3FiAwHTURUXe%40Vc%40H%5Bn%40kApAaC))";
const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const fs = require('fs');


const csv_file = "./csv_polylines_municipios/test_polylines_2011_ccaa12.csv"
const lines = fs.readFileSync(csv_file).toString().split("\n");
const date = new Date().toLocaleString().replace(/:/g, '_').replace(/ /g, '_').replace(/\//g, '_');
console.log(date);

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.emulate(devices['iPhone 6']);
    let extractedData = [];

    for (line of lines) {
        if (line.indexOf("NMUN", 1) === -1) {
            const row = extractParamsCsv(line);

            const urlVenta = "https://www.idealista.com/en/areas/venta-viviendas/?shape=" + row.polyLine;
            console.log(urlVenta);
            let data = { fecha: date, cusec: row.cusec, nmun: row.nmun, v_venta: 0, n_venta: 0, v_alql: 0, n_alql: 0 };
            data["_id"] = row.cusec + "--" + date;
            try {
                const extractedVenta = await extractPrize(page, urlVenta);
                data["v_venta"] = extractedVenta.averagePrize;
                data["n_venta"] = extractedVenta.numberOfElements;

            } catch (error) {
                console.log("error");
            }

            const urlAlql = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape=" + row.polyLine;
            try {
                const extractedAlql = await extractPrize(page, urlAlql);
                data["v_alql"] = extractedAlql.averagePrize;
                data["n_alql"] = extractedAlql.numberOfElements;

            } catch (error) {
                console.log("error");
            }
            extractedData.push(data);
            console.log(data);
        }
    }
    saveInCsv(extractedData);

    await browser.close();
})();

extractPrize = async (page, urlVenta) => {
    await page.goto(urlVenta);
    await page.screenshot({ path: 'example.png' });
    const elementPrize = await page.$(".items-average-price");
    const text = await page.evaluate(element => element.textContent, elementPrize);
    averagePrize = text.replace("Average price:", "").replace("eur/m²", "").replace(",", "").trim()

    const elementNumber = await page.$(".h1-simulated");
    const textNumber = await page.evaluate(element => element.textContent, elementNumber);
    numberOfElements = textNumber.replace(" ", "").trim()

    return { averagePrize: averagePrize, numberOfElements: numberOfElements }
}

extractParamsCsv = (line) => {
    splitLine = line.split(";");
    return { cusec: splitLine[1], nmun: splitLine[2], polyLine: splitLine[5] }
}

saveInCsv = (extractedData) => {
    const header = "CUSEC;NMUN;V_VENTA;N_VENTA;V_ALQL;N_ALQL;FECHA\n"
    const outputFilename = csv_file.replace(".csv", "_scraped.csv");
    fs.writeFileSync(outputFilename, header);
    for (let data of extractedData) {
        const newLine = data.cusec + ";" + data.nmun + ";" + data.v_venta + ";" + data.n_venta + ";" + data.v_alql + ";" + data.n_alql + ";" + data.fecha + "\n";
        fs.appendFileSync(outputFilename, newLine);
    }



}