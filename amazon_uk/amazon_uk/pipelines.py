# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem

class DuplicatesPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        url = item['link']
        # Normalizing the URL can be more sophisticated depending on your needs
        normalized_url = url.split('?')[0]  # This will remove any query parameters from the URL
        if normalized_url in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.urls_seen.add(normalized_url)
            return item

class AmazonUkPipeline:
    def process_item(self, item, spider):
        return item


