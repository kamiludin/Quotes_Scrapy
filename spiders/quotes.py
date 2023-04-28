import scrapy
from collections import OrderedDict # to keep the order of the fields


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            item = OrderedDict() # to keep the order of the fields
            item['text'] = quote.css('span.text::text').get()
            item['author'] = quote.css('span small.author::text').get()
            author_detail_url = quote.css('span a::attr(href)').get()
            item['author_detail'] = response.urljoin(author_detail_url)

            yield scrapy.Request(item['author_detail'], meta={'item': item}, callback=self.parse_author)

        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_author(self, response):
        item = response.meta['item'] # get the item from the meta
        item['birthdate'] = response.css('span.author-born-date::text').get()
        item['birthplace'] = response.css('span.author-born-location::text').get()
        item['description'] = response.css('div.author-description::text').get().strip()

        yield item
