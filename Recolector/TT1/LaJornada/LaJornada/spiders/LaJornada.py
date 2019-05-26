import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime 

class laJornadaSpider(CrawlSpider):
    name = 'LaJornada'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://www.jornada.com.mx/ultimas']

    start_urls = ['https://www.jornada.com.mx/ultimas']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="col-sm-12"]/h1/a | //div[@class="col-7 col-md-12"]/h2/a | //div[@class="col-sm-6 col-md-12 ljn-amt-titulo"]/p/a | //div[@class="col-6 ljn-noticia-secundaria"]/h2/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('//*[@id="2-n"]/a/text()').extract()
        mi_item['titulo'] = response.xpath('//div[@class="col-sm-12"]/h1/text()').extract()
        mi_item['autor'] = response.xpath('normalize-space(//span[@itemprop="name"]/text())').extract()
        mi_item['fecha'] = response.xpath('normalize-space(//*[@id="portal-Columns"]/div/div/article/div/div[1]/div/span[1]/span[2])').extract()
        mi_item['noticia'] = response.xpath('normalize-space(//div[@id="content_nitf"])').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
