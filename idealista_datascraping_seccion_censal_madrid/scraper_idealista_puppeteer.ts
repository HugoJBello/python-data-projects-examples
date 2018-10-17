const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const fs = require('fs');
const delay = require('delay');
const Apify = require('apify');
const randomUA = require('modern-random-ua');

export class ScrapperIdealistaPuppeteer {
    json_dir = "json_polylines_municipios";
    files = fs.readdirSync(this.json_dir);
    timoutTimeSearches: number = 1000;
    timoutTimeCapchaDetected: number = 5 * 60 * 1000;
    date: string = "";
    browser: any;
    page: any;

    public main() {
        Apify.main(async () => {
            //files = ["./test_polylines_2011_ccaa12.json"];
            //shuffleArray(files);
            console.log(this.files);
            //const csv_file = "./csv_polylines_municipios/test_polylines_2011_ccaa12.csv"
            this.date = new Date().toLocaleString().replace(/:/g, '_').replace(/ /g, '_').replace(/\//g, '_');
            console.log(this.date);

            for (let json_file of this.files) {
                const municipio = require("./" + this.json_dir + "/" + json_file);
                if (!municipio.municipioScraped) {
                    const cusecs = municipio.cusecs;
                    let extractedData = this.initializeDataForMunicipio(json_file);

                    await this.initalizePuppeteer();

                    let continueScraping = true;
                    let i = 0;
                    while (continueScraping) {
                        let cusec = cusecs[i];
                        let capchaFound = false;
                        let data;
                        if (!cusec.alreadyScraped) {

                            await this.page.setUserAgent(randomUA.generate());
                            await this.page.emulate(devices['iPhone 6']);

                            data = await this.extractDataAlquilerVenta(municipio, cusec);

                            await this.page.waitFor(this.timoutTimeSearches);
                            console.log(data);
                            capchaFound = await this.detectCapcha();
                        }
                        if (!capchaFound) {
                            if (data) { extractedData.push(data); }
                            this.saveDataForMunicipio(extractedData, json_file);

                            if (municipio.cusecs[i]) municipio.cusecs[i].alreadyScraped = true;
                            this.updateFileMunicipio(municipio, this.json_dir);
                            i = i + 1;
                            continueScraping = (i < cusecs.length);
                        }

                    }

                    municipio.alreadyScraped = true;
                    this.updateFileMunicipio(municipio, this.json_dir);
                    //saveInCsv(extractedData);

                    //await browser.close();
                }
            }
        });
    }

    initalizePuppeteer = async () => {
        this.browser = await Apify.launchPuppeteer({
            userAgent: randomUA.generate(),
            headless: true
        });
        this.page = await this.browser.newPage();
    }

    async extractDataAlquilerVenta(municipio: any, cusec: any) {
        const urlVenta = "https://www.idealista.com/en/areas/venta-viviendas/?shape=" + cusec.urlEncoded;
        console.log("extrayendo datos de venta para " + municipio.fileName + " \n" + urlVenta);
        let data: any = { fecha: this.date, cusec: cusec.cusec, nmun: cusec.nmun, v_venta: 0, n_venta: 0, v_alql: 0, n_alql: 0 };
        data["_id"] = cusec.cusec + "--" + this.date;
        try {
            const extractedVenta = await this.extractPrize(urlVenta);
            data["v_venta"] = extractedVenta.averagePrize;
            data["n_venta"] = extractedVenta.numberOfElements;

        } catch (error) {
            console.log("error");
        }
        await this.page.waitFor(this.timoutTimeSearches);

        const urlAlql = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape=" + cusec.urlEncoded;
        console.log("extrayendo datos de alquiler para " + municipio.fileName + " \n" + urlAlql);
        try {
            const extractedAlql = await this.extractPrize(urlAlql);
            data["v_alql"] = extractedAlql.averagePrize;
            data["n_alql"] = extractedAlql.numberOfElements;

        } catch (error) {
            console.log("error");
        }
        return data;
    }

    extractPrize = async (urlVenta: string) => {
        await this.page.goto(urlVenta);
        await this.page.screenshot({ path: 'example.png' });
        const elementPrize = await this.page.$(".items-average-price");
        const text = await this.page.evaluate((element: any) => element.textContent, elementPrize);
        const averagePrize = text.replace("Average price:", "").replace("eur/m²", "").replace(",", "").trim()

        const elementNumber = await this.page.$(".h1-simulated");
        const textNumber = await this.page.evaluate((element: any) => element.textContent, elementNumber);
        const numberOfElements = textNumber.replace(" ", "").trim()

        return { averagePrize: averagePrize, numberOfElements: numberOfElements }
    }

    saveInCsv = (extractedData: any, json_file: string) => {
        const header = "CUSEC;NMUN;V_VENTA;N_VENTA;V_ALQL;N_ALQL;FECHA\n"
        const outputFilename = "./tmp/" + json_file.split("/")[1].replace(".csv", "_scraped.csv");
        fs.writeFileSync(outputFilename, header);
        for (let data of extractedData) {
            const newLine = data.cusec + ";" + data.nmun + ";" + data.v_venta + ";" + data.n_venta + ";" + data.v_alql + ";" + data.n_alql + ";" + data.fecha + "\n";
            fs.appendFileSync(outputFilename, newLine);
        }
    }

    detectCapcha = async () => {
        let found;
        try {
            const pagetxt = await this.page.content();
            found = pagetxt.indexOf('Vaya! parece que estamos recibiendo muchas peticiones', 1) > -1;
            if (found) {
                console.log("--------------------\n Captcha ha saltado!")
                console.log("esperando...");
                this.initalizePuppeteer();
                await this.page.waitFor(this.timoutTimeCapchaDetected);
            }
        } catch (error) {
            return false
        }
        return found;
    }

    updateFileMunicipio = (municipio: any, json_dir: any) => {
        const outputFilename = "./" + json_dir + "/" + municipio.fileName;
        fs.writeFileSync(outputFilename, JSON.stringify(municipio));
    }

    initializeDataForMunicipio = (json_file: any) => {
        let jsonDataFile = json_file.replace(".json", "_scraped.json");
        if (fs.existsSync("tmp/" + jsonDataFile)) {
            return require("./tmp/" + jsonDataFile);
        }
        return [];
    }

    saveDataForMunicipio = (data: any, json_file: any) => {
        let jsonDataFile = json_file.replace(".json", "_scraped.json");
        const outputFilename = "./tmp/" + jsonDataFile;
        fs.writeFileSync(outputFilename, JSON.stringify(data));
    }
}

const scraper = new ScrapperIdealistaPuppeteer();
scraper.main();
