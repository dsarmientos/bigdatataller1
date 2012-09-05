from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


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
        # Follow this links, but don't parse them
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/\.*'))),

        # Extract links matching and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/name/nm[0-9]+/$')), callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/title/tt[0-9]+/$')), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        filename = '-'.join(response.url.split("/")[-3:-1])
        with open(filename, 'wb') as outf:
            outf.write(response.body)
