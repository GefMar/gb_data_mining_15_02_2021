import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ZillowSpider(scrapy.Spider):
    name = "zillow"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/san-francisco-ca/"]
    page_xpaths = {
        "pagination": '//nav[@aria-label="Pagination"]/ul/li/a/@href',
        "ads": '//div[@id="grid-search-results"]/ul/li/article//'
        'a[contains(@class, "list-card-link")]/@href',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser = webdriver.Firefox()

    def _get_follow_xpath(self, response, select_str, callback, **kwargs):
        for link in response.xpath(select_str):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response):
        yield from self._get_follow_xpath(response, self.page_xpaths["pagination"], self.parse)
        yield from self._get_follow_xpath(response, self.page_xpaths["ads"], self.ads_parse)

    def ads_parse(self, response):
        self.browser.get(response.url)
        print(1)
        media_col = self.browser.find_element_by_xpath('//div[@data-media-col="true"]')
        len_photos = media_col.find_elements_by_xpath(
            '//picture[contains(@class, "media-stream-photo")]'
        )
        while True:
            for _ in range(5):
                media_col.send_keys(Keys.PAGE_DOWN)
            photos = media_col.find_elements_by_xpath(
                '//picture[contains(@class, "media-stream-photo")]'
            )
            if len_photos == len(photos):
                break
            len_photos = len(photos)
        print(1)
