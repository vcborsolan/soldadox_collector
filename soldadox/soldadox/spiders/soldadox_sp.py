import scrapy
from ..items import SoldadoxItem


class SoldadoxSpSpider(scrapy.Spider):
    name = 'soldadox_sp'
    allowed_domains = ['sp.olx.com.br']
    start_urls = ['https://sp.olx.com.br/?sf=1']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.94',
        'DEFAULT_REQUEST_HEADERS' : {
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'pt',
        }
    }


    def parse(self, response):

        links = response.xpath('//a[@data-lurker-detail="list_id"]/@href').getall()

        for link in links:
            yield scrapy.Request(
                link,
                callback=self.parse_ad
            )

        npage = response.xpath('//a[@data-lurker-detail="next_page"]/@href').get()

        yield scrapy.Request(
            npage,
            callback=self.parse
        )

    def parse_ad(self, response):

        vehicles = ["Carros, vans e utilitários","Motos" , "Caminhões" , "Ônibus"]

        car = {
            "modelo": response.xpath('//dt[re:test(text(), "Modelo")]/following-sibling::*/text() | //span[re:test(text(), "Modelo")]/following-sibling::*/text()').get() , 
            "marca": response.xpath('//dt[re:test(text(), "Marca")]/following-sibling::*/text() | //span[re:test(text(), "Marca")]/following-sibling::*/text()').get() ,
            "tipo": response.xpath('//dt[re:test(text(), "Tipo de veículo")]/following-sibling::*/text() | //span[re:test(text(), "Tipo de veículo")]/following-sibling::*/text()').get() ,
            "ano":response.xpath('//dt[re:test(text(), "Ano")]/following-sibling::*/text() | //span[re:test(text(), "Ano")]/following-sibling::*/text()').get() ,
            "km": response.xpath('//dt[re:test(text(), "Quilometragem")]/following-sibling::*/text() | //span[re:test(text(), "Quilometragem")]/following-sibling::*/text()').get() ,
            "potencia": response.xpath('//dt[re:test(text(), "Potência do motor")]/following-sibling::*/text() | //span[re:test(text(), "Potência do motor")]/following-sibling::*/text()').get() ,
            "combustivel": response.xpath('//dt[re:test(text(), "Combustível")]/following-sibling::dd/text() | /span[re:test(text(), "Combustível")]/following-sibling::*/text()').get(),
            "cambio": response.xpath('//dt[re:test(text(), "Câmbio")]/following-sibling::dd/text() | //span[re:test(text(), "Câmbio")]/following-sibling::*/text()').get()  ,
            "direcao": response.xpath('//dt[re:test(text(), "Direção")]/following-sibling::*/text() | //span[re:test(text(), "Direção")]/following-sibling::*/text()').get() ,
            "cor": response.xpath('//span[re:test(text(), "Cor")]/following-sibling::*/text() | //dt[re:test(text(), "Cor")]/following-sibling::*/text()').get(),
            "portas": response.xpath('//dt[re:test(text(), "Portas")]/following-sibling::*/text() | //span[re:test(text(), "Portas")]/following-sibling::*/text()').get() ,
            "fplaca": response.xpath('//dt[re:test(text(), "Final de placa")]/following-sibling::*/text() | //span[re:test(text(), "Final de placa")]/following-sibling::*/text()').get() ,
            "cilindrada": response.xpath('//dt[re:test(text(), "Cilindrada")]/following-sibling::*/text() | //span[re:test(text(), "Cilindrada")]/following-sibling::*/text()').get() ,
            "exchange?": response.xpath('//span[re:test(text(), "Aceita troca")]/text()').get()
        } if response.xpath('//span[re:test(text(), "Categoria")]/following-sibling::*/text() | //dt[re:test(text(), "Categoria")]/following-sibling::*/text()').get() in vehicles else "-"

        ad = SoldadoxItem()

        ad['value'] = response.css('h2::text').get() 
        ad['title'] = response.css('h1::text').get()
        ad['publication'] = response.xpath('//span[re:test(text(), "Publicado")]/text()').getall()[1]
        ad['description'] = response.xpath('//p/span/text()').get()
        ad['cod'] = response.xpath('//span[re:test(text(), "cód")]/text()').getall()[1]
        ad['category'] = response.xpath('//span[re:test(text(), "Categoria")]/following-sibling::*/text() | //dt[re:test(text(), "Categoria")]/following-sibling::*/text()').get()
        ad['types'] = response.xpath('//span[re:test(text(), "Tipo")]/following-sibling::*/text() | //dt[re:test(text(), "Tipo")]/following-sibling::*/text()').get()
        ad['images'] = response.xpath('//img[@class="image "]/@src').getall()
        ad['state'] = response.url.split('/')[2][0:2]
        ad['region'] = response.url.split('/')[3].replace('-', ' ')
        ad['subregion'] = response.xpath('//span[re:test(text(), "Município")]/following-sibling::*/text() | //dt[re:test(text(), "Município")]/following-sibling::*/text()').get() 
        ad['cep'] = response.xpath('//span[re:test(text(), "CEP")]/following-sibling::*/text() | //dt[re:test(text(), "CEP")]/following-sibling::*/text()').get()
        ad['neighborhood'] = response.xpath('//span[re:test(text(), "Bairro")]/following-sibling::*/text() | //dt[re:test(text(), "Bairro")]/following-sibling::*/text()').get()
        ad['url'] = response.url
        ad['car'] = car
        
        yield ad