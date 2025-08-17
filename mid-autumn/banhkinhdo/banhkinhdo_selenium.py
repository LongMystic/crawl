from unicodedata import category

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://banhkinhdo.com.vn/"

def main():
    p_id = 0
    product_urls = pd.read_csv("./banhkinhdo/second_level.csv")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get(website)
    driver.maximize_window()
    time.sleep(3)

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

        time.sleep(2)

        product_url = product_urls.iloc[i]["product_url"]
        product_name = product_urls.iloc[i]["product_name"]
        driver.get(product_url)

        image = driver.find_element(By.XPATH, "//div[@class='flickity-slider']//a").get_attribute("href")

        data["product_id"].append(p_id)
        product_name = driver.find_element(By.XPATH, "//h1[@class='product-title product_title entry-title']").get_attribute("innerHTML")
        data["product_name"].append(product_name)
        barcode = None
        try:
            barcode = driver.find_element(By.XPATH,  "//span[@class='sku']").get_attribute("innerHTML")
            barcode = str(barcode)
        except Exception as e:
            pass
        data["barcode"].append(barcode)
        brand = "Kinh Đô"
        data["brand"].append(brand)

        data["image"].append(image)

        try:
            # Find the element by XPath
            elem = driver.find_element(By.XPATH, "//div[@id='tab-description']")

            # Get all descendant text nodes (like Scrapy's //text())
            texts = elem.text.splitlines()

            # Clean up whitespace and join
            product_description = " ".join([t.strip() for t in texts if t.strip()])
            data["description"].append(product_description)
        except Exception as e:
            data["description"].append(None)
        data["url"].append(product_url)



        print(f"Done product number {p_id}")
        p_id += 1

    pd.DataFrame(data).to_csv("data/product_detail.csv", index=False)

if __name__ == "__main__":
    main()