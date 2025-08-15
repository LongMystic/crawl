from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://vpphonghaonline.com.vn/"

def main():
    cate_urls = pd.read_csv('./data/cate_urls.csv')

    p_id = 0

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
        "url": [],
        "category_tree": []
    }

    data1 = {
        "product_url": [],
        "product_img": []
    }

    for i in range(len(cate_urls)):
        cate_url = cate_urls.iloc[i]["cate_url"]
        driver.get(cate_url)


        while 1:

            time.sleep(3)

            for product in driver.find_elements(By.XPATH, "//section[@class='products-view products-view-grid margin-bottom-50 collection_reponsive']/div[1]/div"):
                p_url = product.find_element(By.XPATH,".//div[@class='product-thumbnail']/a").get_attribute("href")
                p_img = product.find_element(By.XPATH,".//div[@class='product-thumbnail']/a/img").get_attribute("src")
                print(p_url)
                print(p_img)
                data1["product_url"].append(p_url)
                data1["product_img"].append(p_img)

            try:
                next_page_btn = driver.find_element(By.XPATH, "//ul[@class='pagination clearfix']/li[last()]/a")
                next_page_btn.click()
            except Exception as e:
                break

    pd.DataFrame(data1).to_csv("./data/product_urls.csv", index=False)


if __name__ == "__main__":
    main()