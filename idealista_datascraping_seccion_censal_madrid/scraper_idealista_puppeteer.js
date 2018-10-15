const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const fs = require('fs');
const delay = require('delay');
const Apify = require('apify');
const randomUA = require('modern-random-ua');


Apify.main(async () => {

    const csv_dir = "csv_polylines_municipios";
    const files = fs.readdirSync(csv_dir);
    //files = ["./test_polylines_2011_ccaa12.csv"];
    //shuffleArray(files);
    console.log(files);
    //const csv_file = "./csv_polylines_municipios/test_polylines_2011_ccaa12.csv"
    const date = new Date().toLocaleString().replace(/:/g, '_').replace(/ /g, '_').replace(/\//g, '_');
    console.log(date);

    for (csv_file of files){
        const lines = fs.readFileSync("./" + csv_dir + "/" + csv_file).toString().split("\n");

        let extractedData = [];
        const browser = await Apify.launchPuppeteer({
            userAgent: randomUA.generate(),
        });
        const page = await browser.newPage();

        for (line of lines) {
            if (line.indexOf("NMUN", 1) === -1) {
                
                // Or you can set user agent for specific page
                //await page.setUserAgent(randomUA.get());
                await page.emulate(devices['iPhone 6']);
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
                    await detectCapcha(page);
                }
                await page.waitFor(2000);

                const urlAlql = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape=" + row.polyLine;
                try {
                    const extractedAlql = await extractPrize(page, urlAlql);
                    data["v_alql"] = extractedAlql.averagePrize;
                    data["n_alql"] = extractedAlql.numberOfElements;

                } catch (error) {
                    console.log("error");
                }
                await page.waitFor(2000);
                extractedData.push(data);
                console.log(data);
                detectCapcha(page);
            }
        }
        saveInCsv(extractedData);

        await browser.close();
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

extractParamsCsv = (line) => {
    splitLine = line.split(";");
    return { cusec: splitLine[1], nmun: splitLine[2], polyLine: splitLine[5] }
}

saveInCsv = (extractedData) => {
    const header = "CUSEC;NMUN;V_VENTA;N_VENTA;V_ALQL;N_ALQL;FECHA\n"
    const outputFilename = "./tmp/" + csv_file.split("/")[1].replace(".csv", "_scraped.csv");
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
    let txt;
    try {
        error = await page.$(".g-recaptcha");
        const text = await page.evaluate(element => element.textContent, error);
        console.log(error);
    } catch (error) {
        console.log("no captcha");
    }
        if (txt) {
        console.log(txt);
        console.log("___________________________________");
        throw new Error("Capcha encontrado");
    }
    
}