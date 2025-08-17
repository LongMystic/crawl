# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

class First_Level_Pipeline:
    def open_spider(self, spider):
        self.csvfile = open('first_level.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = ['cate_name', 'cate_url']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.csvfile.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item


class Second_Level_Pipeline:
    def open_spider(self, spider):
        self.csvfile = open('second_level.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = ['product_name', 'product_url', 'product_image']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.csvfile.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

class Third_Level_Pipeline:
    def open_spider(self, spider):
        self.csvfile = open('third_level.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = ['product_name', 'product_url', 'product_image', 'product_description', 'barcode']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.csvfile.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item