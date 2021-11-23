import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
import scrapy

logger = logging.getLogger(__name__)

class catagory_counter:

    def __init__(self, item_count):
        self.item_count = item_count
        self.catagory_count_log = 10
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('CATAGORY_COUNT_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

        # instantiate the extension object
        ext = cls(item_count)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        
        # return the extension object
        return ext

    def item_scraped(self, item, spider):
        self.items_scraped += 1
     
        if self.items_scraped%self.catagory_count_log == 0:
        	for k in spider.catagory_count.keys():
        		logger.info(k+' : '+str(spider.catagory_count[k]))
