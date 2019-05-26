import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime

class aztecaNoticiasSpider(CrawlSpider):
    name = 'AztecaNoticias'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['http://www.aztecanoticias.com.mx/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['http://www.aztecanoticias.com.mx/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="az_unit az_unit_big az_layout-col_threequarters"]/a | //div[@class="title_nota"]/a | //div[@class="az_unit az_layout-col_quarter"]/a | //div[@class="az_unit"]/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('//div[@class="az_layout whitebg"]/div[@class="az_layout-wrapper"]/h2/text()  | //h2[@class="az_module-title"]/text()').extract()
        mi_item['titulo'] = response.xpath('//div[@class="az_module_note az_module_note-titlewrapper az_layut-col_full"]/h3/text() | //h1/text()').extract()
        mi_item['autor'] = response.xpath('//div[@class="az_module_note-desc"]/p/span[@class="az_unit-credit-author"]/text()').extract()
        mi_item['fecha'] = response.xpath('//div[@class="az_module_note-desc"]/p/span[@class="az_module_note-credit-date"]/text()').extract()
        mi_item['descripcion'] = response.xpath('//div[@class="az_module_note-desc"]/p[@class="az_module_note-teaser"]/text()').extract()
        mi_item['noticia'] = response.xpath('//div[@class="az_module_note-body"]/div/text() | //div[@class="az_module_note-body"]/p/text()').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
