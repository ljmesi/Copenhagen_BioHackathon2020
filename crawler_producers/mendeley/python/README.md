# Directory contents

This directory contains a simple [Scrapy](https://docs.scrapy.org/en/latest/) web crawler for obtaining molecular trajectories data from [Mendeley Data](https://data.mendeley.com/). It isn't strictly necessary to use this kind of web scraper for obtaining the data since there is a [public API](https://dev.mendeley.com/methods/) which might provide the same data. However creating the webscraper was a good initial practice for learning web crawling in Python. 

To run the web scraper navigate to the same directory as where this `README.md` file exists and enter:

```bash
scrapy crawl basic -o mendeley_molecular_trajectories.csv -t csv
# Or
# scrapy crawl basic -o mendeley_molecular_trajectories.json -t json
# scrapy crawl basic -o mendeley_molecular_dynamics.csv -t csv
# scrapy crawl basic -o mendeley_molecular_dynamics.json -t json

```

More information about obtaining other data formats see the [documentation](https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-format-jsonlines).

Files `mendeley_data_scraping.txt` and `mendeley_data_scraping.yml` contain the environment information used for running the scraper.