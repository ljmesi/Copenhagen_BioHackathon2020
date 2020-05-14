/* 
   NOTES:
  
   EVALUATION EXAMPLES FOR PUPPETEER:
   --------------------
   let text = await page.$eval('*', el => el.innerText.split(' '));
   text = text.map(string => {
       return string.replace(/[^\w\s]/gi, '');
   });
   console.log("text:", text);

   let hrefs = await page.evaluate(() => {
       const links = Array.from(document.querySelectorAll('a'));
       return links.map(link => link.href);
   });
   console.log("hrefs:", hrefs);
  
   TRACING OPTIONS:
   ---------------
   await page.tracing.start({
   path: 'trace.json',
   categories: ['devtools.timeline']})
  
*/ 
const puppeteer = require('puppeteer');
// const rp = require('request-promise');
const cheerio = require('cheerio');
const argv = require('yargs')
    .scriptName("crawler.js")
    .option('url', {
        description: 'the url to check',
        alias: 'u',
        type: 'string'
    })
    .option("format", {
        description: 'The format to output the results',
        alias: 'fmt',
        choices: ["csv", "text"],
        default: "text",
        type: 'string'
    })
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
    if (argv.fmt) {
        console.log("output fmt: ", argv.fmt);
    }
    await page.goto(argv.url)
    await page.waitForSelector('div[role=article]');
    const articles = await page.$$eval('div[role=article]', articles => {
        return articles.map(article => {
       return article.innerHTML;
        })
    })

    //TODO: iterate through articles and get studies
    var article_links = [];
    var author_links = []
    const art = articles[0];
    const $ = cheerio.load(art);
    $('a').each((i, link) => { 
        const href = link.attribs.href;
        if (href.match("article")) {
          article_links.push(href);
          }
        if (href.match("authors")) {
            author_links.push(href);
            }
        });

   // await page.tracing.stop();
    study_params = {};
    study_params.studies = [];
    study = {};
    study.article_links = Array.from(new Set(article_links));
    study.author_linkss = Array.from(new Set(author_links));
    study_params.studies.push(study);
    console.log(JSON.stringify(study_params, null, 4));
    await browser.close();
    console.log('done');
})()

