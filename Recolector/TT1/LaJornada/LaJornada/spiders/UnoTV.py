import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime 

class UnoTVSpider(CrawlSpider):
    name = 'UnoTV'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://www.unotv.com/inicio/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.unotv.com/inicio/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//section[@class="article-list"]/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('//meta[@name="nota_categoria"]/@content').extract()
        mi_item['titulo'] = response.xpath('string(//div[@class="article-title"]/h1/text() | //div[@class="titles"]/h1/text())').extract()
        mi_item['autor'] = response.xpath('string(//div[@class="the-meta"]/span[@class="author"]/br/following-sibling::text())').extract()
        mi_item['fecha'] = response.xpath('//div[@class="the-meta"]/span[@class="date"]/text()').extract()
        mi_item['descripcion'] = response.xpath('string(//div[@class="panel-image-meta"]/p)').extract()
        mi_item['noticia'] = response.xpath('//div[@class="panel-article"]/p[@dir="ltr"]//text()').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item