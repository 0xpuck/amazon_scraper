# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem
from urllib.parse import unquote, urlparse, urlunparse
import logging

class DuplicatesPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        logging.info(f"Processing item: {item['link']}")
        url = item['link']

        # Check if the URL is a redirect link from Amazon
        if "www.amazon.co.uk/sspa/click" in url:
            # Extract the destination URL using the 'url' parameter
            url_path = unquote(url.split('url=')[1].split('&')[0])
            url = "https://www.amazon.co.uk" + url_path

        # Normalizing the URL by removing the /ref=... segment and any query parameters
        parsed = urlparse(url)
        normalized_path = '/'.join(segment for segment in parsed.path.split('/') if not segment.startswith('ref='))
        normalized_url = urlunparse((parsed.scheme, parsed.netloc, normalized_path, "", "", ""))

        if normalized_url in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.urls_seen.add(normalized_url)
            item['link'] = normalized_url  # Update the item's link with the purified URL
            return item


class AmazonUkPipeline:
    def process_item(self, item, spider):
        return item


