import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime 

class elUniversalSpider(CrawlSpider):
    name = 'ElUniversal'
    item_count = 0
#Formato de fecha del dia que se realiza la recolección
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://www.eluniversal.com.mx/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.eluniversal.com.mx/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="views-field views-field-views-conditional-2"]/h1/a | //div[@class="views-field views-field-views-conditional-2"]/h2/a | //div[@class="views-field views-field-title"]/h3/a | //div[@class="views-field views-field-field-titulo-abreviado"]/h2/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('//div[@class="nombre-seccion"]/a/text()').extract()
        mi_item['titulo'] = response.xpath('//div[@class="pane-content"]/h1/text()').extract()
        mi_item['autor'] = response.xpath('//div[@class="field-item even"]/text()').extract()
        mi_item['fecha'] = response.xpath('//div[@class="fechap"]/text()').extract()
        mi_item['descripcion'] = response.xpath('normalize-space(//div[@class="field field-name-field-resumen field-type-text-long field-label-hidden"]/text())').extract()
        mi_item['noticia'] = response.xpath('normalize-space(//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"])').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
