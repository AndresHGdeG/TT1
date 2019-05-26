#Importamos las librerias correspondientes
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#Importamos los datos que necesitamos saber de la página web
from scrapy.exceptions import CloseSpider
from LaJornada.items import LajornadaItem
import time
import datetime 

class AnimalPoliticoSpider(CrawlSpider):
    name = 'AnimalPolitico'
    item_count = 0
    dateToday = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
    #Se permitirá obtener información unicamente en este dominio
    allowed_domain = ['https://www.animalpolitico.com/']
    #Aquí será el inicio del Scrapeo
    start_urls = ['https://www.animalpolitico.com/']

    rules = {
		# Será la xpath para poder acceder a cada noticia
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="wrapper"]/div/div[10]/div[1]/div/a[*] | //*[@id="wrapper"]/div/div[13]/div[1]/div/a[*] | //*[@id="wrapper"]/div/div[18]/div[1]/div[1]/div/div[2]/a[*] | //*[@id="wrapper"]/div/div[18]/div[1]/div[3]/div/div[2]/a[*] | //*[@id="wrapper"]/div/div[18]/div[2]/div[1]/div[3]/a[*] | //*[@id="wrapper"]/div/div[18]/div[2]/div[2]/div/div[2]/a[*]')),
                            callback= 'parse_item', follow= False)
    }
    
    def parse_item(self, response):
        mi_item = LajornadaItem()

        mi_item['url'] = response.url
        mi_item['titulo'] = response.xpath('//div[@class="ap_single_first_title"][1]/text()').extract()
        mi_item['autor'] = response.xpath('(//div[@class="ap_single_first_info_author"]/strong/text())[1]').extract()
        mi_item['fecha'] = response.xpath('normalize-space((//div[@class="ap_single_first_info_date"]/text())[1])').extract()
        mi_item['descripcion'] = response.xpath('//div[@class="ap_single_content"]/p[1]/text()').extract()
        mi_item['noticia'] = response.xpath('(//div[@class="ap_single_content"])[1]/p/text()').extract()
        self.item_count += 1
        if self.item_count >50:
            raise CloseSpider('item_exceeded')
        yield mi_item
