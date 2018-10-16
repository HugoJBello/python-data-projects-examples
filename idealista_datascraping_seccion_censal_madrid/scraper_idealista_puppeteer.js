const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const fs = require('fs');
const delay = require('delay');
const Apify = require('apify');
const randomUA = require('modern-random-ua');


Apify.main(async () => {

    const json_dir = "json_polylines_municipios";
    const files = fs.readdirSync(json_dir);
    //files = ["./test_polylines_2011_ccaa12.json"];
    //shuffleArray(files);
    console.log(files);
    //const csv_file = "./csv_polylines_municipios/test_polylines_2011_ccaa12.csv"
    const date = new Date().toLocaleString().replace(/:/g, '_').replace(/ /g, '_').replace(/\//g, '_');
    console.log(date);

    for (json_file of files) {
        const municipio = require("./" + json_dir + "/" + json_file);
        if (!municipio.municipioScraped) {
            const cusecs = municipio.cusecs;
            let extractedData = initializeDataForMunicipio(json_file);
            const browser = await Apify.launchPuppeteer({
                userAgent: randomUA.generate(),
                headless: true
            });
            const page = await browser.newPage();

            let continueScraping = true;
            let data;
            let i = 0;
            while (continueScraping) {
                console.log("scraping");
                let cusec = cusecs[i];
                let capchaFound = false;
                if (!cusec.alreadyScraped) {
                    // Or you can set user agent for specific page
                    await page.setUserAgent(randomUA.generate());
                    await page.emulate(devices['iPhone 6']);

                    const urlVenta = "https://www.idealista.com/en/areas/venta-viviendas/?shape=" + cusec.urlEncoded;
                    console.log("extrayendo datos de venta para " + municipio.fileName + " \n" + urlVenta);
                    data = { fecha: date, cusec: cusec.cusec, nmun: cusec.nmun, v_venta: 0, n_venta: 0, v_alql: 0, n_alql: 0 };
                    data["_id"] = cusec.cusec + "--" + date;
                    try {
                        const extractedVenta = await extractPrize(page, urlVenta);
                        data["v_venta"] = extractedVenta.averagePrize;
                        data["n_venta"] = extractedVenta.numberOfElements;

                    } catch (error) {
                        console.log("error");
                    }
                    await page.waitFor(10);

                    const urlAlql = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape=" + cusec.urlEncoded;
                    console.log("extrayendo datos de alquiler para " + municipio.fileName + " \n" + urlAlql);
                    try {
                        const extractedAlql = await extractPrize(page, urlAlql);
                        data["v_alql"] = extractedAlql.averagePrize;
                        data["n_alql"] = extractedAlql.numberOfElements;

                    } catch (error) {
                        console.log("error");
                    }
                    await page.waitFor(10);
                    console.log(data);
                    capchaFound = await detectCapcha(page);
                }
                if (!capchaFound) {
                    i = i + 1;
                    continueScraping = (i < cusecs.length);

                    extractedData.push(data);
                    saveDataForMunicipio(extractedData, json_file);

                    if(municipio.cusecs[i]) municipio.cusecs[i].alreadyScraped = true;
                    updateFileMunicipio(municipio, json_dir);
                }

            }

            municipio.alreadyScraped = true;
            updateFileMunicipio(municipio, json_dir);
            //saveInCsv(extractedData);

            //await browser.close();
        }
    }
});

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

saveInCsv = (extractedData) => {
    const header = "CUSEC;NMUN;V_VENTA;N_VENTA;V_ALQL;N_ALQL;FECHA\n"
    const outputFilename = "./tmp/" + json_file.split("/")[1].replace(".csv", "_scraped.csv");
    fs.writeFileSync(outputFilename, header);
    for (let data of extractedData) {
        const newLine = data.cusec + ";" + data.nmun + ";" + data.v_venta + ";" + data.n_venta + ";" + data.v_alql + ";" + data.n_alql + ";" + data.fecha + "\n";
        fs.appendFileSync(outputFilename, newLine);
    }
}

//https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
shuffleArray = (array) => {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

detectCapcha = async (page) => {
    let found;
    try {
        const pagetxt = await page.content();
        found = pagetxt.indexOf('Vaya! parece que estamos recibiendo muchas peticiones', 1) > -1;
        if (found){
            console.log("--------------------\n Captcha ha saltado!")
            console.log("esperando...");
            await page.waitFor(30000);
        } 
    } catch (error) {
        return false
    }
    return found;
}

updateFileMunicipio = (municipio, json_dir) => {
    const outputFilename = "./" + json_dir + "/" + municipio.fileName;
    fs.writeFileSync(outputFilename, JSON.stringify(municipio));
}

initializeDataForMunicipio = (json_file) => {
    let jsonDataFile = json_file.replace(".json", "_scraped.json");
    if (fs.existsSync("tmp/" + jsonDataFile)) {
        return require("./tmp/" + jsonDataFile);
    }
    return [];
}

saveDataForMunicipio = (data, json_file) => {
    let jsonDataFile = json_file.replace(".json", "_scraped.json");
    const outputFilename = "./tmp/" + jsonDataFile;
    fs.writeFileSync(outputFilename, JSON.stringify(data));
}