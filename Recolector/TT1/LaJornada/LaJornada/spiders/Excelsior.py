import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#Importamos los datos que necesitamos saber de la página web
from LaJornada.items import LajornadaItem
import time
import datetime 

class excelsiorSpider(CrawlSpider):
    name = 'Excelsior'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    allowed_domain = ['https://www.excelsior.com.mx/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.excelsior.com.mx/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="stage-list"]/li/a | //*[@id="noticias-principales"]/div/div/a | //*[@id="mas-notas-flujo"]/li/a | //*[@id="lista-notas-destacadas"]/li/a | //*[@id="e-list-ultima-hora"]/li/a | //*[@id="e-list-lomas-leido"]/li/a')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()
        
        mi_item['url'] = response.url
        mi_item['titulo'] = response.xpath('//header/h1/text() | //h1[@class="node-title"]/text()').extract()
        mi_item['autor'] = response.xpath('normalize-space(//*[@id="node-content-ads"]/article/header/span[1]/text() | //*[@id="node-top--bar"]/date/span[@class="user-name"]/text())').extract()
        mi_item['fecha'] = response.xpath('normalize-space(//*[@id="node-content-ads"]/article/header/span[1]/span/text() | //*[@id="node-top--bar"]/date/text())').extract()
        mi_item['descripcion'] = response.xpath('normalize-space(//header/h2/text() | //h1[@class="node-title"]/text())').extract()
        mi_item['noticia'] = response.xpath('normalize-space(//div[@id="node-article-body"])').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item