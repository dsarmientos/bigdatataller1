from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        'http://www.imdb.com/title/tt0107211/',
	'http://www.imdb.com/name/nm0000193/',
	'http://www.imdb.com/list/v58pud2k-f8/',
    ]
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/\.*'))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/name/nm[0-9]+/$')), callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(allow=(r'www.imdb.com/title/tt[0-9]+/$')), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        filename = '-'.join(response.url.split("/")[-3:-1])
        with open(filename, 'wb') as outf:
            outf.write(response.body)
