const puppeteer = require('puppeteer');
// const rp = require('request-promise');
// const $ = require('cheerio');
const argv = require('yargs')
        .scriptName("crawler.js")
        .option('url', {
            description: 'the url to check',
            alias: 'u',
            type: 'string'})
        .option("format", {
        description: 'The format to output the results',
        alias: 'fmt',
        choices: ["csv", "text"],
        default: "text",
        type: 'string'})
        .help()
        .alias('help', 'h')
        .argv;
console.log("crawler starting ");
(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox'],
    timeout: 10000,
  })
  const page = await browser.newPage()
  await page.goto(argv.url)
  const title = await page.title()
  if (argv.fmt) {
      console.log("output fmt: ", argv.fmt);
  }
  console.log(title)
  await browser.close()
})()