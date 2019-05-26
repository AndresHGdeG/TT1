import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime 

class sopitasSpider(CrawlSpider):
    name = 'Sopitas'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://www.sopitas.com/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.sopitas.com/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//h3[@class="post-title m-0"]/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('//meta[@property="article:section"]/@content').extract()
        mi_item['titulo'] = response.xpath('//figcaption/h1/text()').extract()
        mi_item['autor'] = response.xpath('string(//a[@rel="author"])').extract()
        mi_item['fecha'] = response.xpath('string(//p[@class="m-0"]/time)').extract()
        mi_item['noticia'] = response.xpath('normalize-space(//*/p[@style="text-align: justify;"]| //article)').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item