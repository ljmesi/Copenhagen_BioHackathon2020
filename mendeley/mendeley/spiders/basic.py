# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Spider
import json
from mendeley.items import MendeleyItem

class BasicSpider(Spider):
    name = 'basic'
    base_url = 'https://data.mendeley.com/api/research-data/search?search=molecular%20trajectories&type=DATASET&page='
    #base_url = 'https://data.mendeley.com/api/research-data/search?search=Molecular%20Dynamics&type=DATASET&page='
    page_no = 1
    start_urls = [base_url + str(page_no)]
    
    def parse(self, response):
        # jsonify the response body
        data = json.loads(response.body.decode(encoding = 'utf-8'))
        results = data.get('results')
        # Check if results list is empty
        if results:
            for result in results:
                item = MendeleyItem()
                try:
                    item['externalSubjectAreas'] = '|'.join(result.get('externalSubjectAreas'))
                except TypeError as error:
                    print(error)
                    item['externalSubjectAreas'] = None
                try:
                    item['keywords'] = '|'.join(result.get('containerKeywords'))
                except TypeError as error:
                    print(error)
                    item['keywords'] = None
                try:
                    item['institutions'] = '|'.join(result.get('institutions'))
                except TypeError as error:
                    print(error)
                    item['institutions'] = None
                try:
                    item['authors'] = '|'.join([author['name'] for author in result.get('authors')])
                except TypeError as error:
                    print(error)
                    item['authors'] = None
                try:
                    item['dataTypes'] = '|'.join(result.get('containerDataTypes'))
                except TypeError as error:
                    print(error)
                    item['dataTypes'] = None

                item['title'] = result.get('containerTitle')
                item['description'] = result.get('containerDescription')
                item['doi'] = result.get('doi')
                item['publicationDate'] = result.get('publicationDate')
                item['dateAvailable'] = result.get('dateAvailable')
                item['version'] = result.get('version')
                item['accessRights'] = result.get('accessRights')
                item['containerURI'] = result.get('containerURI')
                item['method'] = result.get('method')
                item['source'] = result.get('source')
                item['type_cont'] = result.get('containerType')
                yield item
    
            # Retain next page url        
            self.page_no += 1
            next_page = self.base_url + str(self.page_no)
            print("\nScaping: ", next_page, "\n")
            yield response.follow(next_page, callback=self.parse)

