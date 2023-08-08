import scrapy


class AmazonUKSpider(scrapy.Spider):
    name = 'amazon_uk'
    allowed_domains = ['www.amazon.co.uk']
    # filter_word = None

    def start_requests(self):
        search_term = getattr(self, 'search', 'Intel NUC')  # Default to 'Intel NUC' if no search term is provided
        category = getattr(self, 'category', 'computers')  # Default to 'computers' if no category is provided
        self.filter_word = getattr(self, 'filter_word', None)  # Default to None if no filter is provided
        url = f'https://www.amazon.co.uk/s?k={search_term}&i={category}'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extract product details from the search results page
        product_elements = response.css('[data-asin]')
        for product_element in product_elements:
            asin = product_element.attrib['data-asin']
            if asin:
                name = product_element.css('span.a-size-medium.a-color-base.a-text-normal::text').get()
                price = product_element.css('span.a-price .a-offscreen::text').get()
                if name and self.filter_word and self.filter_word.lower() not in name.lower():
                    continue
                if not price:
                    continue
                else:
                    voucher = product_element.css(
                        'span.a-size-base.s-highlighted-text-padding.aok-inline-block.s-coupon-highlight-color::text').get()

                    # Extract product link
                    link = product_element.css('a.a-link-normal::attr(href)').get()
                    if link:  # Make the link absolute if it's relative
                        link = response.urljoin(link)

                    yield {
                        'asin': asin,
                        'filter': self.filter_word if self.filter_word else 'No filter',
                        'name': name,
                        'price': price,
                        'voucher': voucher if voucher else 'No voucher',
                        'link': link
                        # Add more fields as needed
                    }
            else:
                continue

        # Follow pagination links if available
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
