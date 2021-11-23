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

        # connect the extension object to signals
        #crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        #crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        print(dir(crawler))
        print(dir(signals))

        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s", spider.name)
        logger.info("HEHEHEHEHEHEHEHEHEHEHEHEHEHEH")

    def spider_closed(self, spider):
        logger.info("closed spider %s", spider.name)
        logger.info("HEHEHEHEHEHEHEHEHEHEHEHEHEHEH")

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        #yield scrapy.Request('https://theurge.com/men/search/?page=3&cat=shoes-boots',callback = self.extension_test_parse)
        #print(dir(boots))
        #print(dir(boots.body))
        #print(boots.body)

       # boots_count = int(boots.xpath('//*[@class="_3-VCf"]/text()').re('^\d{0,10}\+')[0].replace('+',''))

        #print('TOTAL BOOTS', boots_count)

        #print(spider.make_requests_from_url('https://theurge.com/men/search/?page=3&cat=shoes-boots'))

        if self.items_scraped%self.catagory_count_log == 0:
        	for k in spider.catagory_count.keys():
        		logger.info(k+' : '+str(spider.catagory_count[k]))

    def extension_test_parse(self,response):
        print('KEKEKEKEKEKEKEKE')
        print(response)
        boot_count = int(response.xpath('//*[@class="_3-VCf"]/text()').re('^\d{0,10}\+')[0].replace('+',''))
        print(boot_count)
        return boot_count




