import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime 

class aristeguiNoticiasSpider(CrawlSpider):
    name = 'AristeguiNoticias'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://aristeguinoticias.com/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://aristeguinoticias.com/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="class_notas_int"] | //div[@class="class_ultimas_noticias"]/div[@class="parrafo_noticias"] | //span[@class="col"]/ul/li')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url 
        mi_item['titulo'] = response.xpath('//div[@class="class_subtitular"]/h1/text() | //div[@class="class_subtitular"]/text()').extract()
        mi_item['autor'] = response.xpath('//div[@class="share_nom"]/text()').extract()
        mi_item['fecha'] = response.xpath('//div[@class="share_publicado"]/text()').extract()
        mi_item['descripcion'] = response.xpath('//div[@class="class_text2"]/text()').extract()
        mi_item['noticia'] = response.xpath('normalize-space(//div[@class="class_text"])').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
