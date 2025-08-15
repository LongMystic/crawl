from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://thienlong.vn/"


def main():
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
        # "category_tree": []
    }
    val = 0
    p_id = 500
    stop_val = 750
    start_time = time.time()
    for i in range(len(product_urls)):
        if i < p_id:
            print(f"IGNORE P_ID: {i}")
            continue

        # if p_id == stop_val:
        #     break

        time.sleep(1)

        product_url = product_urls.iloc[i]["product_url"]
        product_img = product_urls.iloc[i]["product_img"]
        try:
            driver.get(product_url)
        except Exception as e:
            continue

        data["product_id"].append(p_id)
        product_name = driver.find_element(By.XPATH, "//h1[@class='title-product']").get_attribute("innerHTML")
        data["product_name"].append(product_name)
        sku = None
        try:
            sku = driver.find_element(By.XPATH, "//p[@class='product_sku first_status']/span").get_attribute(
                "innerHTML")
            sku = str(sku)
        except Exception as e:
            pass
        data["sku"].append(sku)
        brand = None
        try:
            brand = driver.find_element(By.XPATH,
                                        "//span[@class='first_status']/span[@class='status_name']").get_attribute(
                "innerHTML")
            brand = str(brand).strip()
        except Exception as e:
            pass
        data["brand"].append(brand)

        try:
            product_img_urls = ""
            for img in driver.find_elements(By.XPATH,
                                            "//div[@class='section slickthumb_relative_product_1']//div[@class='slick-track']/div"):
                img_url = img.find_element(By.XPATH, "./a/img").get_attribute("src")
                if len(product_img_urls) > 1:
                    img_url = f"*****{img_url}"
                product_img_urls += img_url
            data["image"].append(product_img_urls)
        except Exception as e:
            data["image"].append(product_img)

        price = None
        try:
            cur_price = driver.find_element(By.XPATH, "//span[@class='special-price']/span").get_attribute("innerHTML")
            price = cur_price
        except Exception as e:
            pass
        try:
            old_price = driver.find_element(By.XPATH, "//span[@class='old-price']/del").get_attribute("innerHTML")
            price = old_price
        except Exception as e:
            pass

        data["price"].append(price)
        try:
            product_description = driver.find_element(By.XPATH,
                                                      "//div[@class='description ui-tabs ui-widget ui-widget-content ui-corner-all']/div[1]").get_attribute(
                "innerHTML")
            data["description"].append(product_description)
        except Exception as e:
            data["description"].append(None)
        data["url"].append(product_url)

        print(f"Done product number {p_id}")
        p_id += 1

    print(f"END WITH TIME: {time.time() - start_time}")
    pd.DataFrame(data).to_csv(f"./data/product_detail_{stop_val}.csv", index=False)


if __name__ == "__main__":
    main()