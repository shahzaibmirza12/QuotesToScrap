from scrapy import Request, Spider


class quotesSpider(Spider):
    name = 'quotes'
    start_urls = ["https://quotes.toscrape.com"]
    base_url = ["https://quotes.toscrape.com"]
    custom_settings = {
        'FEED_URI': "Quotes.csv",
        'FEED_FORMAT': 'csv'
    }

    # get value from terminal =>scrapy crawl quotes -a value=shahzaib
    def parse(self, response):
        print(self.value)
        for data in response.css('.quote'):
            yield {
                'Quote': data.css('.text::text').get(),
                'Auther': data.css('.author::text').get(),
                'Tags': data.css('.tag::text').getall(),
            }
        yield from self.parse_next_page(response)

    def parse_next_page(self, response):
        data = response.css('li.next > a::attr(href)').extract_first()
        if data:
            yield Request(self.base_url[0] + data, self.parse)
