from unicodedata import category

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://bachhoalanhao.com/collections/banh-trung-thu"

def main():
    p_id = 0
    product_urls = pd.read_csv("./data/product.csv")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get(website)
    driver.maximize_window()
    time.sleep(1)

    data = {
        "product_id": [],
        "product_name": [],
        "barcode": [],
        "brand": [],
        "image": [],
        "description": [],
        "url": []
    }

    for i in range(len(product_urls)):

        time.sleep(1)

        product_url = product_urls.iloc[i]["product_image"]
        product_image = product_urls.iloc[i]["product_url"]
        driver.get(product_url)

        product_name = driver.find_element(By.XPATH, "//h1[@class='product-name font-weight-bold mb-2 d-inline-flex mr-3']").get_attribute("innerHTML")
        # product_brand = driver.find_element(By.XPATH, "//div[@class='pro-brand']/a").get_attribute("innerHTML")
        # if product_brand is None or product_brand == '':
        product_brand = 'Kinh Đô'
        barcode = driver.find_element(By.XPATH, "//span[@id='sku']").get_attribute("innerHTML")

        data["product_name"].append(product_name)
        data["brand"].append(product_brand)
        data["description"].append(None)
        data["image"].append(product_image)
        data["url"].append(product_url)
        data["product_id"].append(p_id)
        data["barcode"].append(barcode)



        print(f"Done product number {p_id}")
        p_id += 1

    pd.DataFrame(data).to_csv("./data/product_detail.csv", index=False)

if __name__ == "__main__":
    main()