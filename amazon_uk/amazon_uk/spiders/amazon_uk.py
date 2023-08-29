import scrapy
from ..items import AmazonUkItem


class AmazonUKSpider(scrapy.Spider):
    name = 'amazon_uk'
    allowed_domains = ['www.amazon.co.uk']


    def __init__(self, search="Intel NUC", category="computers", filter_words="", exception_keywords="", filter_mode="all", *args, **kwargs):
        super(AmazonUKSpider, self).__init__(*args, **kwargs)
        self.search_term = search
        self.category = category
        self.filter_words = [word.strip() for word in filter_words.split(',')] if filter_words else []
        self.exception_keywords = [word.strip() for word in exception_keywords.split(',')] if exception_keywords else []
        self.filter_mode = filter_mode

    def start_requests(self):
        url = f'https://www.amazon.co.uk/s?k={self.search_term}'
        if self.category:
            url += f'&i={self.category}'
        yield scrapy.Request(url, callback=self.parse)

    def contains_exception_keywords(self, name):
        """Check if the product name contains any exception keyword."""
        return any(keyword.lower() in name.lower() for keyword in self.exception_keywords)

    def contains_filter_words(self, name):
        """Check if the product name contains filter words based on the selected filter_mode."""
        name_cf = name.casefold()
        match self.filter_mode:
            case "any":
                return any(word.lower().casefold() in name_cf for word in self.filter_words)
            case _:
                return all(word.lower().casefold() in name_cf for word in self.filter_words)

    def parse(self, response):
        # Extract product details from the search results page
        product_elements = response.css('[data-asin]')
        for product_element in product_elements:
            asin = product_element.attrib['data-asin']
            if asin:
                name_parts = product_element.css('span.a-size-medium.a-color-base::text').getall()
                name = ''.join(name_parts).strip()
                price = product_element.css('span.a-price .a-offscreen::text').get()
                voucher = product_element.css(
                    'span.a-size-base.s-highlighted-text-padding.aok-inline-block.s-coupon-highlight-color::text').get()
                # Extract product link
                link = product_element.css('a.a-link-normal::attr(href)').get()
                if link:  # Make the link absolute if it's relative
                    link = response.urljoin(link)

                if (name and price and
                        self.contains_filter_words(name) and
                        not self.contains_exception_keywords(name)):
                    item = AmazonUkItem()
                    item['asin'] = asin
                    item['filter'] = ', '.join(self.filter_words) if self.filter_words else 'No filter'
                    item['name'] = name
                    item['price'] = price
                    item['voucher'] = voucher if voucher else 'No voucher'
                    item['link'] = link

                    yield item
            else:
                continue

        # Follow pagination links if available
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)


