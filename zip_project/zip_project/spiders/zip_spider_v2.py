import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from zip_project.items import The_Urge_Item
from scrapy.loader.processors import MapCompose, Join
import datetime
import logging
import yaml

logger = logging.getLogger('mycustomlogger')

class ZipSpiderV2Spider(CrawlSpider):

    fpath = 'the_urge_todo.yaml'
    with open(fpath,'r') as file:
        job_params = yaml.safe_load(file)

    name = str(job_params['name'])
    
    start_urls = job_params['start_urls']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=job_params['paginate_down_page']), callback='parse_item'), #Paginiation down page
        Rule(LinkExtractor(restrict_xpaths=job_params['paginate_horizontally']), callback='parse_item') #Paginiation across catagories
    )    
    
    def __init__(self, *a, **kw):
        super(ZipSpiderV2Spider, self).__init__(*a, **kw)
        self.response_count_var = 0

        fpath = 'the_urge_todo.yaml'
        with open(fpath,'r') as file:
            self.job_params = yaml.safe_load(file)
        
    def parse_item(self,response): ## method for adding more fields
        self.response_count_var +=1
        
        self.manage_catagory_count(response) # Steps required for tracking total items in each catagory

        l = ItemLoader(item = The_Urge_Item(),response = response)


        for item in self.job_params['items']:
            if 're' in item.keys() and 'string_replacements' in item.keys():
                l.add_xpath(item['fieldName'],item['xpath'],MapCompose(lambda i: i.replace(item['string_replacements'][0], item['string_replacements'][1]), float),re =item['re'])
            elif 're' in item.keys():
                l.add_xpath(item['fieldName'],item['xpath'],re =item['re'])
            elif 'string_replacements' in item.keys():
                l.add_xpath(item['fieldName'],item['xpath'],MapCompose(lambda i: i.replace(item['string_replacements'][0], item['string_replacements'][1]), float))
            else:
                l.add_xpath(item['fieldName'],item['xpath'])

        l.add_value('date',datetime.datetime.now())
        
        #Logs latency
        logger.info('Download time: %.4f - %.4f = %.4f seconds' % (response.meta['__end_time'], response.meta['__start_time'],response.meta['__end_time'] - response.meta['__start_time']))
        return l.load_item()

    def manage_catagory_count(self,response):
        if self.response_count_var == 1: #If this is the spiders first request then create catagory count variable.
            self.catagory_urls = response.xpath(self.job_params['catagory_url']).extract()
            self.catagory_count = {}
            for cat in self.catagory_urls:
                self.catagory_count[cat] = None
        else:
            if 'page=' in response.url:
                url_key = str(response.url).replace(re.findall('page=\d{0,10}&',url_test2)[0],'').replace(self.job_params['start_urls'][0][:-1],'')
            else:
                url_key = str(response.url).replace(self.job_params['start_urls'][0][:-1],'')
            self.catagory_count[url_key] = int(response.xpath(self.job_params['toal_catagory_items']).re('^\d{0,10}')[0])
