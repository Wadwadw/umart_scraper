import scrapy
from scrapy.loader import ItemLoader
from ..items import UmartItem

class ScrapSpider(scrapy.Spider):
    name = 'scrap'
    allowed_domains = ['www.umart.com.au']
    dom = 'https://www.umart.com.au/'


    def start_requests(self):
        yield scrapy.Request(
            url='https://www.umart.com.au/brand.html',
            callback=self.parse_all_brand

        )
        yield scrapy.Request(url='https://www.umart.com.au/Apple_152B.html',
                             callback=self.parse_brand
                             )

    def parse_all_brand(self, response):
        categories = response.xpath("//div[@class='container-fluid all_brands_cat']/div/div/div[contains(@class,'col-xs-12')]/ul/li")
        for category in categories:
            url = category.xpath(".//a/@href").get()
            full_url = self.dom + str(url)
            yield scrapy.Request(url=full_url,
                                 callback=self.parse_brand
                                 )

    def parse_brand(self, response):
        item_urls = response.xpath("//li[@class='goods_info']")
        for item_url in item_urls:
            url = item_url.xpath(".//div[contains(@class,'row')]/div[@class='col-xs-8 col-sm-11']/div/div/div/a/@href").get()
            full_url = self.dom + str(url)
            is_in_stock = item_url.xpath(".//div[contains(@class,'row')]/div[@class='col-xs-8 col-sm-11']/div/div[contains(@class,'content_holder2')]/div/span[@class='goods_stock graphik-bold']/font/b/text()").get()
            sku = item_url.xpath(".//@data-id").get()
            yield scrapy.Request(url=full_url,
                                 callback=self.parse_item,
                                 meta={'is_in_stock': is_in_stock,
                                       'sku': sku
                                       }
                                 )


        next_page = response.xpath("(//ul[contains(@class,'page')]/li[last()])[2]")
        if next_page:
            next_page_url = next_page.xpath(".//a/@href").get()
            full_url = self.dom + str(next_page_url)
            yield scrapy.Request(url=full_url,
                                 callback=self.parse_brand
                                 )

    def parse_item(self, response):
        loader = ItemLoader(item=UmartItem())
        url = response.url
        base_url = 'umart.com.au'
        sku = response.request.meta['sku']
        mpn = response.xpath("//div[@itemprop='mpn']/text()").get()
        title = response.xpath("//h1[@itemprop='name']/text()").get()
        price_in_tax = response.xpath("//span[@class='graphik-bold']/span[@class='goods-price']/text()").get()
        is_in_stock = response.request.meta['is_in_stock']
        if 'In Stock' in is_in_stock:
            is_in_stock = 'true'
        else:
            is_in_stock = 'false'

        loader.add_value('Url', url)
        loader.add_value('BaseUrl', base_url)
        loader.add_value('SKU', sku)
        loader.add_value('MPN', mpn)
        loader.add_value('Model', mpn)
        loader.add_value('Title', title)
        loader.add_value('PriceIncTax', price_in_tax)
        loader.add_value('IsInStock', is_in_stock)
        loader.add_value('QuantityAvailable', 'Null')
        yield loader.load_item()
