import re
from typing import List
import logging

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver as WDriver
from selenium.webdriver.remote.webelement import WebElement as WElement

from crawler_lib.article import Article, File
from crawler_lib.browser_automation import wait_for_child_article_link, wait_for_article_div

JS_QUERYSELECTOR = "return document.querySelectorAll('{selector}')"
FIGSHARE_PARENT_ARTICLE_QUERY = JS_QUERYSELECTOR.format(selector='a[class*=linkback-url]')
FIGSHARE_KEYWORD_QUERY = JS_QUERYSELECTOR.format(selector='a[href*=keyword]')
FIGSHARE_DOCUMENT_QUERY = JS_QUERYSELECTOR.format(selector='a[title*=Download]')
FIGSHARE_DOI_QUERY = JS_QUERYSELECTOR.format(selector='div[data-doi]')
FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE = "return document.querySelectorAll('span')"

# TODO: remove unused constants
# FIGSHARE_ALL_XPATH = ".//*"
# FIGSHARE_ANCHOR_XPATH = ".//a"
FIGSHARE_DOWNLOAD_XPATH = ".//div"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

DATE_REGEX = r'.*([0-9]{2}[.][0-9]{2}[.][0-9]{4}).*'


class AbstractWebParser(object):
    def __init__(self):
        pass

    @staticmethod
    def parse_all_text_elements_in_page(element: WElement) -> List[str]:
        text = element.find_element_by_xpath(".//*").text
        text_list = text.split('\n')
        return text_list

    @staticmethod
    def parse_all_links_in_page(element: WElement) -> str:
        return element.find_element_by_xpath(".//a").get_attribute("href")


class FigshareWebParser(AbstractWebParser):
    def __init__(self):
        super().__init__()

    def parse_text_list(self, text_list: List[str]):
        if len(text_list) == 4:
            # TODO: try to capture article type
            # article_type = text_list[0]
            title = text_list[1]
            posted_on_text = text_list[2]
            author = text_list[3]
            log.info("author from 4 list found: " + author)
            article = self.build_article_from_author_list(author, posted_on_text, title)
            log.info("current author list: " + str(article.authors))
            return article
        if len(text_list) == 3:
            author = text_list[-1]
            posted_on_text = text_list[-2]
            log.info("author from 3 list found: " + author)
            article = self.build_article_from_author_list(author, posted_on_text, text_list[-3])
            log.info("current author list: " + str(article.authors))
            return article
        if len(text_list) >= 5:
            author = text_list[-1]
            posted_on_text = text_list[-2]
            log.info("author from 3 list found: " + author)
            article = self.build_article_from_author_list(author, posted_on_text, text_list[-3])
            log.info("current author list: " + str(article.authors))
            return article
        log.info("no length match for text: ", text_list)

    def parse_file_obj(self, driver: WDriver) -> List[File]:
        log.info("parsing file objects")
        file_list = []
        try:
            file_url_query = driver.execute_script(FIGSHARE_DOCUMENT_QUERY)
            file_doi_query = driver.execute_script(FIGSHARE_DOI_QUERY)

            file_download_links = [x.get_attribute('href') for x in file_url_query]
            page_start = 5
            page_end = 15
            div_xpath = driver.find_element_by_xpath(FIGSHARE_DOWNLOAD_XPATH).text.splitlines()
            page_info = div_xpath[page_start:-page_end]
            log.info("page info: " + str(page_info))
            downloads_cite_index = div_xpath.index("Cite")
            downloads_start = div_xpath.index("Explore more content")
            file_descriptions = div_xpath[downloads_start:downloads_cite_index]
            log.info("file descriptions: " + file_descriptions)
            file_name = div_xpath[ downloads_cite_index - 1 ]
            log.info("file name: " + file_name)
            #DEBUGGING
            #log.info("file_download_links: " + str(file_download_links))
            for url in file_download_links:
                file_name = None if len(file_url_query) < 1 else file_url_query[0].text
                log.info("file name from document query: " + file_name)
                file_list.append(self.build_file_obj(file_name,
                                                     None if len(file_url_query) < 1 else file_doi_query[0].get_attribute('data-doi'),
                                                     url))
        except Exception:
            log.info("could not parse file object attribute from element", exc_info=True)
        return file_list

    @staticmethod
    def parse_upload_date(date_text: str) -> str:
        date_match = re.match(DATE_REGEX, date_text)
        return None if date_match is None else date_match.group(1)

    @staticmethod
    def parse_keywords(driver: WDriver) -> List[str]:
        keywords = list()
        keyword_element_list = driver.execute_script(FIGSHARE_KEYWORD_QUERY)
        for kw_element in keyword_element_list:
            keywords.append(kw_element.get_attribute('title'))
        return keywords

    def parse_parent_article(self, driver: WDriver) -> Article:
        wait_for_child_article_link(driver)
        child_article_js_query = FIGSHARE_PARENT_ARTICLE_QUERY
        if child_article_js_query == None:
            log.error("child article query failed")
            return
        article_element_list = driver.execute_script(child_article_js_query)
        return self.build_child_article(article_element_list[0].get_attribute('innerHTML'),
                                        article_element_list[0].get_attribute('href').strip("https://doi.org/"),
                                        article_element_list[0].get_attribute('href'))

    # TODO: kill this method
    @staticmethod
    def parse_total_pages_from_span(driver) -> str:
        wait_for_article_div(driver)
        span_list = driver.execute_script(FIGSHARE_ARTICLE_JS_QUERY_PAGE_SIZE)
        for span in span_list:
            span_text = span.text
            if 'results found' in span_text:
                return str(span_text).split(' ')[0]

    def build_article_from_author_list(self, author, posted_on_text, title):
        return Article(title=title,
                       upload_date=self.parse_upload_date(posted_on_text),
                       authors=[author])

    def build_article_from_element(self, element):
        current_attempt = 0
        while (current_attempt < 3):
            try:
                text_list = self.parse_all_text_elements_in_page(element)
                href = self.parse_all_links_in_page(element)
                article = self.parse_text_list(text_list)
                if article and href and href.startswith("http"):
                    article.source_url = href
                    return article
                else:
                    log.error("could not add source url ")
            except StaleElementReferenceException:
                break
            except Exception as e:
                current_attempt += 1
                log.error("could not build article from element", exc_info=True)
                if ('text_list' in locals()):
                    log.info("text list: \n", text_list, "\n\n")

    @staticmethod
    def build_child_article(actual_article_doi, actual_article_title, actual_article_url):
        return Article(title=actual_article_title, source_url=actual_article_url,
                       digital_object_id=actual_article_doi, published=True, enriched=True)

    @staticmethod
    def build_file_obj(file_name, file_doi_string, file_url):
        return File(file_name=file_name,
                    digital_object_id=file_doi_string,
                    url=file_url)
