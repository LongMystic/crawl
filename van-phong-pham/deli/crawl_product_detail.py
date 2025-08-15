from unicodedata import category

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://vppdeli.vn/"

def main():
    p_id = 0
    product_urls = pd.read_csv("./data/product_urls.csv")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get(website)
    driver.maximize_window()
    time.sleep(3)

    data = {
        "product_id": [],
        "product_name": [],
        "sku": [],
        "brand": [],
        "image": [],
        "price": [],
        "description": [],
        "url": [],
        "category_tree": []
    }

    for i in range(len(product_urls)):

        time.sleep(2)

        product_url = product_urls.iloc[i]["product_url"]
        product_img = product_urls.iloc[i]["product_img"]
        driver.get(product_url)

        data["product_id"].append(p_id)
        product_name = driver.find_element(By.XPATH, "//h1[@class='product-title product_title entry-title']").get_attribute("innerHTML")
        data["product_name"].append(product_name)
        sku = None
        try:
            sku = driver.find_element(By.XPATH,  "//span[@class='sku']").get_attribute("innerHTML")
            sku = str(sku)
        except Exception as e:
            pass
        data["sku"].append(sku)
        brand = "Deli"
        try:
            brand = driver.find_element(By.XPATH, "//div[@class='group-status']/span[1]/span[@class='status_name']").get_attribute("innerHTML")
            brand = str(brand)
        except Exception as e:
            pass
        data["brand"].append(brand)

        # try:
        #     product_img_urls = ""
        #     for img in driver.find_elements(By.XPATH, "//div[@class='swiper-wrapper']/div"):
        #         img_url = img.find_element(By.XPATH, "./a/img").get_attribute("src")
        #         if len(product_img_urls) > 1:
        #             img_url = f"*****{img_url}"
        #         product_img_urls += img_url
        #     data["image"].append(product_img_urls)
        # except Exception as e:
        #     pass
        data["image"].append(product_img)

        price = None
        try:
            price = driver.find_element(By.XPATH, "//p[@class='price product-page-price ']/span/bdi").get_attribute("innerHTML")
        except Exception as e:
            pass
        data["price"].append(price)
        try:
            product_description = driver.find_element(By.XPATH, "//div[@class='woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content active']").get_attribute("innerHTML")
            data["description"].append(product_description)
        except Exception as e:
            data["description"].append(None)
        data["url"].append(product_url)

        category_tree = ""
        try:
            for cate in driver.find_elements(By.XPATH, "//nav[@class='woocommerce-breadcrumb breadcrumbs uppercase']/a"):
                cate_val = cate.find_element(By.XPATH, ".").get_attribute("innerHTML")
                if len(category_tree) > 1:
                    cate_val = f" > {cate_val}"
                if cate_val.lower() != 'home':
                    category_tree += cate_val
            print(category_tree)

        except Exception as e:
            print(e)
        data["category_tree"].append(category_tree)

        print(f"Done product number {p_id}")
        p_id += 1

    pd.DataFrame(data).to_csv("data/product_detail-2.csv", index=False)

if __name__ == "__main__":
    main()