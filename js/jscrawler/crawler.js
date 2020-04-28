const puppeteer = require('puppeteer');
//TODO: move to args
const url = 'https://figshare.com/search?q=dcd&searchMode=1';
// const rp = require('request-promise');
// const $ = require('cheerio');
console.log("crawler starting ");
(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox'],
    timeout: 10000,
  })
  const page = await browser.newPage()
  await page.goto(url)
  const title = await page.title()
  console.log(title)
  await browser.close()
})()
