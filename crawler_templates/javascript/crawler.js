const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const argv = require('yargs')
    .scriptName("crawler.js")
    .option('url', {
        description: 'the url to check',
        alias: 'u',
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
    await page.goto(argv.url)

    //TODO: iterate through articles and get studies
    // as an example:
    // studyParams = {};
    // studyParams.studies = [];
    // await page.waitForSelector('div[role=article]');
    // // return all innerHTML for articles
    // const articles = await page.$$eval('div[role=article]', articles => {
    //     return articles.map(article => {
    //    return article.innerHTML;
    //     })
    // })
    // for (var i =0; articles.size(); i++) {
    //   const $ = cheerio.load(articles[i]);
    //   $('a').each((i, link) => { 
    //       const href = link.attribs.href;
    //       if (href.match("article")) {
    //         sourceUrl = href;
    //         }
    //       if (href.match("authors")) {
    //           authorLinks.push(href);
    //           }
    //       });
    //   study = buildStudy(sourceUrl, authorLinks);
    //   studyParams.studies.push(study);
    // }
    // console.log(JSON.stringify(study_params, null, 4));
    let hrefs = await page.evaluate( () => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.map(link => link.href);
        });
    console.log('hrefs:', hrefs);
    //TODO: send message to aws sqs service when finished

    await browser.close();
    console.log('done');

})()

function buildStudyParams(sourceUrl, authorLinks) {
    study = {};
    study.sourceUrl = sourceUrl, 
    study.authorLinks = Array.from(new Set(authorLinks));
    return study;
}

