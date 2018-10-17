const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const fs = require('fs');
const delay = require('delay');
const Apify = require('apify');
const randomUA = require('modern-random-ua');
import { ConvertCsvRawFilesToJson } from './ConvertCsvRawFilesToJson'

export class ScrapperIdealistaPuppeteer {
    json_dir = "json_polylines_municipios";
    outputTempDir = "tmp/";
    config = require("./scraping_config.json");
    files = fs.readdirSync(this.json_dir);
    timoutTimeSearches: number = 1000;
    timoutTimeCapchaDetected: number = 5 * 60 * 1000;
    sessionId: string = this.config.sessionId;
    convertCsvRawFilesToJson: ConvertCsvRawFilesToJson = new ConvertCsvRawFilesToJson();
    MongoClient = require('mongodb').MongoClient;

    date: string = "";
    browser: any;
    page: any;

    public async finalizeSession() {
        this.sessionId = "scraping" + "----" + this.date;
        this.config.sessionId = this.sessionId;
        fs.writeFileSync('scraping_config.json', JSON.stringify(this.config));
        await this.convertCsvRawFilesToJson.convert();
    }

    public initializeSession() {
        this.date = new Date().toLocaleString().replace(/:/g, '_').replace(/ /g, '_').replace(/\//g, '_');
        this.outputTempDir = this.outputTempDir + this.sessionId + "/";
        this.sessionId = this.config.sessionId;
        console.log("\n-------------------------------------------------------");
        console.log(this.sessionId);
        console.log("\n-------------------------------------------------------");

    }

    public main() {
        Apify.main(async () => {
            this.initializeSession();
            //files = ["./test_polylines_2011_ccaa12.json"];
            console.log(this.files);
            //const csv_file = "./csv_polylines_municipios/test_polylines_2011_ccaa12.csv"
            console.log(this.date);

            for (let json_file of this.files) {
                const municipio = require("./" + this.json_dir + "/" + json_file);
                if (!municipio._id) { municipio._id = this.sessionId; }
                if (!municipio.municipioScraped) {
                    const cusecs = municipio.cusecs;
                    let extractedData: ExtractedData = this.initializeDataForMunicipio(json_file);

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
                            if (data) { extractedData.scrapedData.push(data); }
                            this.saveDataForMunicipio(extractedData, json_file);

                            if (municipio.cusecs[i]) municipio.cusecs[i].alreadyScraped = true;
                            this.updateFileMunicipio(municipio, this.json_dir);
                            i = i + 1;
                            continueScraping = (i < cusecs.length);
                        }

                    }

                    municipio.municipioScraped = true;
                    if (this.config.useMongoDb){await this.insertExtractedDataMongo(extractedData);}
                    this.updateFileMunicipio(municipio, this.json_dir);
                    this.saveInCsv(extractedData, json_file);

                    //await browser.close();
                }
            }

            await this.finalizeSession();
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

    saveInCsv = (extractedData: ExtractedData, json_file: string) => {
        if (json_file) {
            const header = "CUSEC;NMUN;V_VENTA;N_VENTA;V_ALQL;N_ALQL;FECHA\n"
            const outputFilename = "./" + this.outputTempDir + json_file.replace(".json", "_scraped.csv");
            fs.writeFileSync(outputFilename, header);
            for (let data of extractedData.scrapedData) {
                let newLine;
                if (data.cusec) {
                    newLine = data.cusec + ";" + data.nmun + ";" + data.v_venta + ";" + data.n_venta + ";" + data.v_alql + ";" + data.n_alql + ";" + data.fecha + "\n";
                    fs.appendFileSync(outputFilename, newLine);

                }
            }
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
                await this.page.waitFor(this.timoutTimeCapchaDetected);
                await this.initalizePuppeteer();

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

    public initializeDataForMunicipio(json_file: any): ExtractedData {
        let jsonDataFile = json_file.replace(".json", "_scraped.json");
        let nmun: string = json_file.split("_")[0];
        if (fs.existsSync(this.outputTempDir + " /" + jsonDataFile)) {
            let data = require("./" + this.outputTempDir + jsonDataFile);
            data._id = nmun + "--" + this.sessionId
            if (!data.nmun) { data.nmun = nmun; }
            return data;
        }
        const extractedData: ExtractedData = { _id: nmun + "--" + this.sessionId, sessionId: this.sessionId, nmun: nmun, scrapedData: [] };
        return extractedData;
    }

    saveDataForMunicipio = (data: any, json_file: any) => {
        let jsonDataFile = json_file.replace(".json", "_scraped.json");
        if (!fs.existsSync(this.outputTempDir)) {
            fs.mkdirSync(this.outputTempDir);
        }
        const outputFilename = "./" + this.outputTempDir + jsonDataFile;
        fs.writeFileSync(outputFilename, JSON.stringify(data));
    }

    async insertExtractedDataMongo(extractedData:ExtractedData){
        await this.MongoClient.connect(this.config.mongoUrl, function(err:any, client:any) {
            const db = "realstate-db";
            const collectionName = "summaries";
            console.log("saving data in mongodb");
            const collection = client.db(db).collection(collectionName);
            collection.save(extractedData);
            client.close();
         });
    }
}


export interface ExtractedData {
    _id: string;
    sessionId: string;
    nmun: string;
    scrapedData: CusecData[];
}

export interface CusecData {
    fecha: string;
    cusec: number,
    nmun: string,
    v_venta: number,
    n_venta: number,
    v_alql: number,
    n_alql: number,
    _id: string
}


//------------------MAIN PROGRAM-------------------------
const scraper = new ScrapperIdealistaPuppeteer();
scraper.main();
