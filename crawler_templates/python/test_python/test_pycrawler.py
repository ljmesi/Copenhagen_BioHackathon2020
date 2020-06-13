import unittest
import json
#from unittest.mock import patch, sentinel

class CrawlerTest(unittest.TestCase):

    def json_validator(self, data):
        try:
            json.loads(data)
            return True
        except ValueError as error:
            print("invalid json: %s" % error)
            return False

    def test_application_start(self):
        try:
            from crawler_templates.python.pycrawler import run
        except Exception as e:
            from pycrawler import run
        test_url = "https://google.com"
        result = run(test_url)
        self.assertTrue(self.json_validator(json.dumps(result)))

if __name__ == '__main__':
    unittest.main()
