"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var puppeteer = require('puppeteer');
var devices = require('puppeteer/DeviceDescriptors');
var fs = require('fs');
var delay = require('delay');
var Apify = require('apify');
var randomUA = require('modern-random-ua');
var ScrapperIdealistaPuppeteer = /** @class */ (function () {
    function ScrapperIdealistaPuppeteer() {
        var _this = this;
        this.json_dir = "json_polylines_municipios";
        this.files = fs.readdirSync(this.json_dir);
        this.timoutTimeSearches = 10;
        this.timoutTimeCapchaDetected = 30 * 1000;
        this.date = "";
        this.initalizePuppeteer = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this;
                        return [4 /*yield*/, Apify.launchPuppeteer({
                                userAgent: randomUA.generate(),
                                headless: true
                            })];
                    case 1:
                        _a.browser = _c.sent();
                        _b = this;
                        return [4 /*yield*/, this.browser.newPage()];
                    case 2:
                        _b.page = _c.sent();
                        return [2 /*return*/];
                }
            });
        }); };
        this.extractPrize = function (urlVenta) { return __awaiter(_this, void 0, void 0, function () {
            var elementPrize, text, averagePrize, elementNumber, textNumber, numberOfElements;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.page.goto(urlVenta)];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, this.page.screenshot({ path: 'example.png' })];
                    case 2:
                        _a.sent();
                        return [4 /*yield*/, this.page.$(".items-average-price")];
                    case 3:
                        elementPrize = _a.sent();
                        return [4 /*yield*/, this.page.evaluate(function (element) { return element.textContent; }, elementPrize)];
                    case 4:
                        text = _a.sent();
                        averagePrize = text.replace("Average price:", "").replace("eur/m²", "").replace(",", "").trim();
                        return [4 /*yield*/, this.page.$(".h1-simulated")];
                    case 5:
                        elementNumber = _a.sent();
                        return [4 /*yield*/, this.page.evaluate(function (element) { return element.textContent; }, elementNumber)];
                    case 6:
                        textNumber = _a.sent();
                        numberOfElements = textNumber.replace(" ", "").trim();
                        return [2 /*return*/, { averagePrize: averagePrize, numberOfElements: numberOfElements }];
                }
            });
        }); };
        this.saveInCsv = function (extractedData, json_file) {
            var header = "CUSEC;NMUN;V_VENTA;N_VENTA;V_ALQL;N_ALQL;FECHA\n";
            var outputFilename = "./tmp/" + json_file.split("/")[1].replace(".csv", "_scraped.csv");
            fs.writeFileSync(outputFilename, header);
            for (var _i = 0, extractedData_1 = extractedData; _i < extractedData_1.length; _i++) {
                var data = extractedData_1[_i];
                var newLine = data.cusec + ";" + data.nmun + ";" + data.v_venta + ";" + data.n_venta + ";" + data.v_alql + ";" + data.n_alql + ";" + data.fecha + "\n";
                fs.appendFileSync(outputFilename, newLine);
            }
        };
        this.detectCapcha = function () { return __awaiter(_this, void 0, void 0, function () {
            var found, pagetxt, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 4, , 5]);
                        return [4 /*yield*/, this.page.content()];
                    case 1:
                        pagetxt = _a.sent();
                        found = pagetxt.indexOf('Vaya! parece que estamos recibiendo muchas peticiones', 1) > -1;
                        if (!found) return [3 /*break*/, 3];
                        console.log("--------------------\n Captcha ha saltado!");
                        console.log("esperando...");
                        this.initalizePuppeteer();
                        return [4 /*yield*/, this.page.waitFor(this.timoutTimeCapchaDetected)];
                    case 2:
                        _a.sent();
                        _a.label = 3;
                    case 3: return [3 /*break*/, 5];
                    case 4:
                        error_1 = _a.sent();
                        return [2 /*return*/, false];
                    case 5: return [2 /*return*/, found];
                }
            });
        }); };
        this.updateFileMunicipio = function (municipio, json_dir) {
            var outputFilename = "./" + json_dir + "/" + municipio.fileName;
            fs.writeFileSync(outputFilename, JSON.stringify(municipio));
        };
        this.initializeDataForMunicipio = function (json_file) {
            var jsonDataFile = json_file.replace(".json", "_scraped.json");
            if (fs.existsSync("tmp/" + jsonDataFile)) {
                return require("./tmp/" + jsonDataFile);
            }
            return [];
        };
        this.saveDataForMunicipio = function (data, json_file) {
            var jsonDataFile = json_file.replace(".json", "_scraped.json");
            var outputFilename = "./tmp/" + jsonDataFile;
            fs.writeFileSync(outputFilename, JSON.stringify(data));
        };
    }
    ScrapperIdealistaPuppeteer.prototype.main = function () {
        var _this = this;
        Apify.main(function () { return __awaiter(_this, void 0, void 0, function () {
            var _i, _a, json_file, municipio, cusecs, extractedData, continueScraping, i, cusec, capchaFound, data;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        //files = ["./test_polylines_2011_ccaa12.json"];
                        //shuffleArray(files);
                        console.log(this.files);
                        //const csv_file = "./csv_polylines_municipios/test_polylines_2011_ccaa12.csv"
                        this.date = new Date().toLocaleString().replace(/:/g, '_').replace(/ /g, '_').replace(/\//g, '_');
                        console.log(this.date);
                        _i = 0, _a = this.files;
                        _b.label = 1;
                    case 1:
                        if (!(_i < _a.length)) return [3 /*break*/, 12];
                        json_file = _a[_i];
                        municipio = require("./" + this.json_dir + "/" + json_file);
                        if (!!municipio.municipioScraped) return [3 /*break*/, 11];
                        cusecs = municipio.cusecs;
                        extractedData = this.initializeDataForMunicipio(json_file);
                        return [4 /*yield*/, this.initalizePuppeteer()];
                    case 2:
                        _b.sent();
                        continueScraping = true;
                        i = 0;
                        _b.label = 3;
                    case 3:
                        if (!continueScraping) return [3 /*break*/, 10];
                        cusec = cusecs[i];
                        capchaFound = false;
                        data = void 0;
                        if (!!cusec.alreadyScraped) return [3 /*break*/, 9];
                        return [4 /*yield*/, this.page.setUserAgent(randomUA.generate())];
                    case 4:
                        _b.sent();
                        return [4 /*yield*/, this.page.emulate(devices['iPhone 6'])];
                    case 5:
                        _b.sent();
                        return [4 /*yield*/, this.extractDataAlquilerVenta(municipio, cusec)];
                    case 6:
                        data = _b.sent();
                        return [4 /*yield*/, this.page.waitFor(10)];
                    case 7:
                        _b.sent();
                        console.log(data);
                        return [4 /*yield*/, this.detectCapcha()];
                    case 8:
                        capchaFound = _b.sent();
                        _b.label = 9;
                    case 9:
                        if (!capchaFound) {
                            i = i + 1;
                            continueScraping = (i < cusecs.length);
                            extractedData.push(data);
                            this.saveDataForMunicipio(extractedData, json_file);
                            if (municipio.cusecs[i])
                                municipio.cusecs[i].alreadyScraped = true;
                            this.updateFileMunicipio(municipio, this.json_dir);
                        }
                        return [3 /*break*/, 3];
                    case 10:
                        municipio.alreadyScraped = true;
                        this.updateFileMunicipio(municipio, this.json_dir);
                        _b.label = 11;
                    case 11:
                        _i++;
                        return [3 /*break*/, 1];
                    case 12: return [2 /*return*/];
                }
            });
        }); });
    };
    ScrapperIdealistaPuppeteer.prototype.extractDataAlquilerVenta = function (municipio, cusec) {
        return __awaiter(this, void 0, void 0, function () {
            var urlVenta, data, extractedVenta, error_2, urlAlql, extractedAlql, error_3;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        urlVenta = "https://www.idealista.com/en/areas/venta-viviendas/?shape=" + cusec.urlEncoded;
                        console.log("extrayendo datos de venta para " + municipio.fileName + " \n" + urlVenta);
                        data = { fecha: this.date, cusec: cusec.cusec, nmun: cusec.nmun, v_venta: 0, n_venta: 0, v_alql: 0, n_alql: 0 };
                        data["_id"] = cusec.cusec + "--" + this.date;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.extractPrize(urlVenta)];
                    case 2:
                        extractedVenta = _a.sent();
                        data["v_venta"] = extractedVenta.averagePrize;
                        data["n_venta"] = extractedVenta.numberOfElements;
                        return [3 /*break*/, 4];
                    case 3:
                        error_2 = _a.sent();
                        console.log("error");
                        return [3 /*break*/, 4];
                    case 4: return [4 /*yield*/, this.page.waitFor(10)];
                    case 5:
                        _a.sent();
                        urlAlql = "https://www.idealista.com/en/areas/alquiler-viviendas/?shape=" + cusec.urlEncoded;
                        console.log("extrayendo datos de alquiler para " + municipio.fileName + " \n" + urlAlql);
                        _a.label = 6;
                    case 6:
                        _a.trys.push([6, 8, , 9]);
                        return [4 /*yield*/, this.extractPrize(urlAlql)];
                    case 7:
                        extractedAlql = _a.sent();
                        data["v_alql"] = extractedAlql.averagePrize;
                        data["n_alql"] = extractedAlql.numberOfElements;
                        return [3 /*break*/, 9];
                    case 8:
                        error_3 = _a.sent();
                        console.log("error");
                        return [3 /*break*/, 9];
                    case 9:
                        console.log(data);
                        return [2 /*return*/, data];
                }
            });
        });
    };
    return ScrapperIdealistaPuppeteer;
}());
exports.ScrapperIdealistaPuppeteer = ScrapperIdealistaPuppeteer;
var scraper = new ScrapperIdealistaPuppeteer();
scraper.main();
