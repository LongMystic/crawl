from unicodedata import category

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://baothymart.com/banh-trung-thu"

def main():
    p_id = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get(website)
    driver.maximize_window()
    time.sleep(3)

    data = {
        "product_image": [],
        "product_url": []
    }

    while True:

        time.sleep(2)

        for product in driver.find_elements(By.XPATH, "//div[@class='products row row-small large-columns-5 medium-columns-3 small-columns-2 has-equal-box-heights']/div"):
            product_image = product.find_element(By.XPATH, ".//div[@class='image-none']/a").get_attribute("href")
            product_url = product.find_element(By.XPATH, ".//div[@class='image-none']/a//img").get_attribute("src")
            
            data["product_image"].append(product_image)
            data["product_url"].append(product_url)

        try:
            next_btn = driver.find_element(By.XPATH, "//span[@class='nextPage']/a")
            next_btn.click()
        except Exception as e:
            print("Cannot move to next page. Cancel crawl here!!!")
            break

        # print(f"Done product number {p_id}")
        # p_id += 1

    pd.DataFrame(data).to_csv("./data/product.csv", index=False)

if __name__ == "__main__":
    main()