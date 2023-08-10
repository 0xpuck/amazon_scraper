import scrapy


class AmazonUKSpider(scrapy.Spider):
    name = 'amazon_uk'
    allowed_domains = ['www.amazon.co.uk']

    def __init__(self, exception_keywords=None, *args, **kwargs):
        # Note: Corrected the super call's class name to match the class itself
        super(AmazonUKSpider, self).__init__(*args, **kwargs)
        self.exception_keywords = exception_keywords.split(',') if exception_keywords else []

    def contains_exception_keywords(self, name):
        """Check if the product name contains any exception keyword."""
        return any(keyword.lower() in name.lower() for keyword in self.exception_keywords)

    # Removed the misplaced if condition from here

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
                name_parts = product_element.css('span.a-size-medium.a-color-base::text').getall()
                name = ''.join(name_parts).strip()
                price = product_element.css('span.a-price .a-offscreen::text').get()
                voucher = product_element.css(
                    'span.a-size-base.s-highlighted-text-padding.aok-inline-block.s-coupon-highlight-color::text').get()
                # Extract product link
                link = product_element.css('a.a-link-normal::attr(href)').get()
                if link:  # Make the link absolute if it's relative
                    link = response.urljoin(link)

                # Moved the condition inside the for loop where name and price are defined
                if (name and price and
                        (not self.filter_word or self.filter_word.lower() in name.lower()) and
                        not self.contains_exception_keywords(name)):
                    yield {
                        'asin': asin,
                        'filter': self.filter_word if self.filter_word else 'No filter',
                        'name': name,
                        'price': price,
                        'voucher': voucher if voucher else 'No voucher',
                        'link': link
                    }
            else:
                continue

        # Follow pagination links if available
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
