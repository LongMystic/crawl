import scrapy


class First_Level_Spider(scrapy.Spider):
    name = "first_level"
    allowed_domains = ["banhkinhdo.com.vn"]
    start_urls = ["https://banhkinhdo.com.vn/danh-muc-san-pham/banh-afc-keo-choco/"]

    def parse(self, response):
        for row in response.xpath("//ul[@class='product-categories']/li"):

            cate_name = row.xpath('./a/text()').get()

            cate_url = row.xpath('./a/@href').get()

            print(cate_name, cate_url)
            if cate_name is not None and cate_name != 'None':
                yield {
                    'cate_name': cate_name,
                    'cate_url': cate_url,
                }

