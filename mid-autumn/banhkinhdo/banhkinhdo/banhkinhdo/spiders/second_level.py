import scrapy
import pandas as pd

parent = []


class Second_Level_Spider(scrapy.Spider):
    name = "second_level"
    allowed_domains = ["banhkinhdo.com.vn"]
    start_urls = ["https://banhkinhdo.com.vn/danh-muc-san-pham/banh-afc-keo-choco/"]

    def start_requests(self):
        cate_url_list = pd.read_csv("first_level.csv")
        for url in cate_url_list["cate_url"]:
            for i in range(1, 4):
                try:
                    yield scrapy.Request(url=f"{url}page/{i}/", callback=self.parse)
                except Exception as e:
                    print("URL NOT FOUND")
                    print(e)

    def parse(self, response):
        for row in response.xpath("//div[@class='products row row-small large-columns-4 medium-columns-3 small-columns-2 has-shadow row-box-shadow-2 has-equal-box-heights equalize-box']/div"):
            product_name = row.xpath(".//div[@class='product-small box ']//a/@aria-label").get()
            product_url = row.xpath(".//div[@class='product-small box ']//a/@href").get()
            product_image = row.xpath(".//div[@class='product-small box ']//img/@data-src | .//div[@class='product-small box ']//img/@src").get()
            if product_name is not None and product_name != 'None':
                yield {
                    'product_name': product_name,
                    'product_url': product_url,
                    'product_image': product_image
                }
