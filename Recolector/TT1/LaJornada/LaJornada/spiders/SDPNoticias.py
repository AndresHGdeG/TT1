import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime

class sdpNoticiasSpider(CrawlSpider):
    name = 'SDPNoticias'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://www.sdpnoticias.com/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.sdpnoticias.com/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//h3/a | //*/li/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('//span[@class="cont-seccion"]/text()').extract()
        mi_item['titulo'] = response.xpath('normalize-space(//h1/text())').extract()
        mi_item['autor'] = response.xpath('normalize-space(//span[@class="cont-agencias"] | //span[@class="autor"]/text())').extract()
        mi_item['fecha'] = response.xpath('normalize-space(//div[@class="cont-info"]/span[@class="fecha"]/text())').extract()
        mi_item['descripcion'] = response.xpath('//p[@class="cont-extracto"]/text() | //div[@class="descripcion"]/text()').extract()
        mi_item['noticia'] = response.xpath('//div[@class="cont-cuerpo"]/p/text() | //p/text()').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
