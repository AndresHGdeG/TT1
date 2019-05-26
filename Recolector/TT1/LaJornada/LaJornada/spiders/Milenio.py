#Importamos las librerias correspondientes
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#Importamos los datos que necesitamos saber de la página web
from scrapy.exceptions import CloseSpider
from LaJornada.items import LajornadaItem
import time
import datetime

class MilenioSpider(CrawlSpider):
    name = 'Milenio'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    #Se permitirá obtener información unicamente en este dominio
    allowed_domain = ['https://www.milenio.com/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.milenio.com/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="title"]/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()

        mi_item['url'] = response.url
        mi_item['seccion'] = response.xpath('normalize-space(//*[@id="main-header"]/div[3]/div/ul/li[1]/a[2]/text())').extract()
        mi_item['titulo'] = response.xpath('//h1[@class="title"]/text()').extract()
        mi_item['autor'] = response.xpath('//span[@class="author"]/text()').extract()
        mi_item['fecha'] = response.xpath('//time/text()').extract()
        mi_item['descripcion'] = response.xpath('//span[@class="summary"]/text()').extract() 
        mi_item['noticia'] = response.xpath('//div[@id="content-body"]/p//text()').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
