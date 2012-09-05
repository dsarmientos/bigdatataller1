import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


def extract_base_links(value):
    m = re.search(
        r'http://(www\.imdb\.com/(?:(?:title/tt)|(?:name/nm))[0-9]+).*',
        value)
    if m:
        return m.group(1)
    else:
        return value


class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        'http://www.imdb.com/name/nm0461498/',
        'http://www.imdb.com/name/nm0004747/',
        'http://www.imdb.com/name/nm0001834/',
        'http://www.imdb.com/name/nm0018554/',
        'http://www.imdb.com/name/nm0412382/',
    ]
    rules = (
        # Extract links matching and parse them with the spider's method
        Rule(SgmlLinkExtractor(
            allow=(r'www.imdb.com/name/nm[0-9]+/$')),
            callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(
            allow=(r'www.imdb.com/title/tt[0-9]+/$')),
            callback='parse_page', follow=True),
        # Follow this links, and extract new links to crawl
        Rule(
            SgmlLinkExtractor(
                allow=(r'www.imdb.com/\.*',),
                process_value=extract_base_links),
	    follow=True
        ),
    )

    def parse_page(self, response):
        filename = '-'.join(response.url.split("/")[-3:-1])
        with open(filename, 'wb') as outf:
            outf.write(response.body)
