from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

website = "https://www.fahasa.com/"

def main():
    # cate_id = 0
    data = {
        "cate_url": [],
        "cate_name": []
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get(website)
    driver.maximize_window()
    time.sleep(3)

    val = 0
    stop_val = 4

    for row in driver.find_elements(By.XPATH, "//ul[@class='nav navbar-nav verticalmenu']/li"):
        try:
            # data["cate_id"].append(cate_id)
            cate_url = row.find_element(By.XPATH, "./a").get_attribute("href")
            cate_name = row.find_element(By.XPATH, "./a").get_attribute("title")
            # print(str(cate_id) + " " + cate_url)
            data["cate_url"].append(cate_url)
            data["cate_name"].append(cate_name)
            # cate_id += 1
        except Exception as e:
            pass

        val += 1
    print(data)
    pd.DataFrame(data).to_csv("./data/cate_urls.csv", index=False)

if __name__ == "__main__":
    main()