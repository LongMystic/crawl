from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://vpphonghaonline.com.vn/"

def main():
    # cate_id = 0
    data = {
        "cate_url": []
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get(website)
    driver.maximize_window()
    time.sleep(3)

    val = 0
    stop_val = 4

    for row in driver.find_elements(By.XPATH, "//ul[@class='nav nav_1']/li"):
        if val == stop_val:
            break
        for cate in row.find_elements(By.XPATH, "./ul/li"):
            try:
                # data["cate_id"].append(cate_id)
                cate_url = cate.find_element(By.XPATH, "./a").get_attribute("href")
                # print(str(cate_id) + " " + cate_url)
                data["cate_url"].append(cate_url)
                # cate_id += 1
            except Exception as e:
                pass

        val += 1
    data["cate_url"].append("https://vpphonghaonline.com.vn/tui-vai")
    print(data)
    pd.DataFrame(data).to_csv("./data/cate_urls.csv", index=False)

if __name__ == "__main__":
    main()