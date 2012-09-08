import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


def extract_base_links(value):
    m = re.search(
        r'http://www\.imdb\.com(/(?:(?:title/tt)|(?:name/nm))[0-9]+/).*',
        value)
    if m:
        return m.group(1)


class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        'http://www.imdb.com/',
    ]
    rules = (
        # Extract links matching and parse them with the spider's method
        Rule(
            SgmlLinkExtractor(allow=(r'www.imdb.com/name/nm[0-9]+/$')),
            callback='parse_page',
            follow=True),
        Rule(
            SgmlLinkExtractor(allow=(r'www.imdb.com/title/tt[0-9]+/$')),
            callback='parse_page',
            follow=True),
        # Follow this links
        Rule(
            SgmlLinkExtractor(allow=(r'www.imdb.com/\.*',)),
	    follow=True),
        # Extract new links to parse
        Rule(
            SgmlLinkExtractor(
                allow= r'http://www\.imdb\.com/(?:(?:title/tt)|(?:name/nm))[0-9]+/.+',
                process_value=extract_base_links),
            follow=True),
    )

    def parse_page(self, response):
        filename = '-'.join(response.url.split("/")[-3:-1])
        with open(filename, 'wb') as outf:
            outf.write(response.body)
