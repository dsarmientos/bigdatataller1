from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        'http://www.imdb.com/name/nm0000221/',
        'http://www.imdb.com/name/nm0674781/',
        'http://www.imdb.com/name/nm0000876/',
        'http://www.imdb.com/name/nm1330560/',
        'http://www.imdb.com/name/nm0107281/',
    ]
    rules = (
        # Follow this links, but don't parse them
        #Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/\.*'))),

        # Extract links matching and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/name/nm[0-9]+/$')), callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/title/tt[0-9]+/$')), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        filename = '-'.join(response.url.split("/")[-3:-1])
        with open(filename, 'wb') as outf:
            outf.write(response.body)
