import scrapy
from ..items import TherugshopscraperItem

class rugshopSpider(scrapy.Spider):
    name = 'rugshop'
    number_page = 2
    start_urls = ['https://www.therugshopuk.co.uk/rugs-by-type/rugs.html']

    def parse(self, response):
        rugs = response.css('.product-item-info')
        for rug in rugs:
            rug_link = rug.css('.product-item-link::attr(href)').get()
            yield response.follow(rug_link, callback = self.get_details)

        next_page = f'https://www.therugshopuk.co.uk/rugs-by-type/rugs.html?p={rugshopSpider.number_page}'
        rugshopSpider.number_page += 1
        if rugshopSpider.number_page < 11:
            yield response.follow(next_page, callback = self.parse)

    def get_details(self, response):
        items = TherugshopscraperItem()

        name = response.css('.base::text').get()
        price = response.css('.act::text').getall()
        rug_id = response.css('.pdp_product_id:nth-child(1)::text').get().replace('Product Id : ', '')
        material = response.css('.prod_mat::text').get().strip()
        rug_link = response.url

        items['name'] = name
        items['price'] = price
        items['rug_id'] = rug_id
        items['material'] = material
        items['rug_link'] = rug_link
        yield items

        