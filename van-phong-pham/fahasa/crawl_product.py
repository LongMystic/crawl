from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import pandas as pd
import time

website = "https://www.fahasa.com/"

def handle_overlays(driver):
    """
    Handle various types of overlays that might appear on the page
    """
    overlay_selectors = [
        ".m-overlay",
        ".overlay",
        ".modal",
        ".popup",
        "#chrome_desktop_backend",
        "[class*='overlay']",
        "[class*='modal']",
        "[class*='popup']",
        ".brz-popup2",  # New overlay type
        ".brz-popup2__overlay",
        "[class*='brz-popup']"
    ]
    
    # First, try to click close buttons for specific overlay types
    close_button_selectors = [
        ".brz-popup2__close",
        ".popup-close",
        ".modal-close",
        ".overlay-close",
        "[class*='close']",
        "button[aria-label*='close']",
        "button[title*='close']"
    ]
    
    for close_selector in close_button_selectors:
        try:
            close_buttons = driver.find_elements(By.CSS_SELECTOR, close_selector)
            for close_btn in close_buttons:
                if close_btn.is_displayed():
                    print(f"Found close button with selector: {close_selector}")
                    try:
                        # Try normal click first
                        close_btn.click()
                        print("Clicked close button successfully")
                        time.sleep(1)
                    except Exception as e:
                        print(f"Normal click failed, trying JavaScript: {e}")
                        try:
                            driver.execute_script("arguments[0].click();", close_btn)
                            print("JavaScript click on close button successful")
                            time.sleep(1)
                        except Exception as js_e:
                            print(f"JavaScript click also failed: {js_e}")
        except Exception as e:
            print(f"Error handling close button with selector {close_selector}: {e}")
            continue
    
    # Then handle the overlays themselves
    for selector in overlay_selectors:
        try:
            overlays = driver.find_elements(By.CSS_SELECTOR, selector)
            for overlay in overlays:
                if overlay.is_displayed():
                    print(f"Overlay detected with selector: {selector}")
                    
                    # Method 1: Try to click outside the overlay
                    try:
                        driver.execute_script("arguments[0].click();", overlay)
                    except:
                        pass
                    
                    # Method 2: Remove overlay using JavaScript
                    try:
                        driver.execute_script("arguments[0].remove();", overlay)
                    except:
                        pass
                    
                    # Method 3: Hide overlay using CSS
                    try:
                        driver.execute_script("arguments[0].style.display = 'none';", overlay)
                    except:
                        pass
                    
                    # Method 4: Set overlay opacity to 0
                    try:
                        driver.execute_script("arguments[0].style.opacity = '0';", overlay)
                    except:
                        pass
                    
                    # Method 5: Set pointer-events to none to prevent click interception
                    try:
                        driver.execute_script("arguments[0].style.pointerEvents = 'none';", overlay)
                    except:
                        pass
                    
                    # Method 6: Set z-index to -1 to move it behind other elements
                    try:
                        driver.execute_script("arguments[0].style.zIndex = '-1';", overlay)
                    except:
                        pass
                    
                    # Method 7: For brz-popup2 specifically, try to trigger dismiss events
                    if 'brz-popup' in selector:
                        try:
                            driver.execute_script("""
                                if (typeof MoeOsm !== 'undefined') {
                                    MoeOsm.dismissMessage('68941903d29335f6d7f2b60e');
                                }
                            """)
                            print("Triggered MoeOsm dismiss for brz-popup")
                        except:
                            pass
                    
                    time.sleep(1)
                    print("Overlay removal attempted")
                    
        except Exception as e:
            print(f"Error handling overlay with selector {selector}: {e}")
            continue
    
    # Additional cleanup: scroll and click body
    try:
        driver.execute_script("window.scrollBy(0, 100);")
        body = driver.find_element(By.TAG_NAME, "body")
        driver.execute_script("arguments[0].click();", body)
    except:
        pass

def force_click_element(driver, element, max_attempts=3):
    """
    Force click an element even if it's intercepted by overlays
    """
    for attempt in range(max_attempts):
        try:
            # First try normal click
            element.click()
            return True
        except Exception as e:
            print(f"Click attempt {attempt + 1} failed: {e}")
            
            # Handle overlays before retrying
            handle_overlays(driver)
            
            # Try JavaScript click as fallback
            try:
                driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as js_e:
                print(f"JavaScript click also failed: {js_e}")
                
                # Try scrolling to element and clicking
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception as scroll_e:
                    print(f"Scroll and click failed: {scroll_e}")
                    
            time.sleep(2)  # Wait before next attempt
    
    return False

def wait_for_page_load(driver, timeout=10):
    """
    Wait for page to load and handle any overlays
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@id='products_grid']"))
        )
    except TimeoutException:
        print("Timeout waiting for products grid")
    
    # Handle overlays after page load
    handle_overlays(driver)

def main():
    cate_urls = pd.read_csv('./data/cate_urls.csv')

    p_id = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # Add additional options to handle overlays
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
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

    t = 1182
    ignore_i = 1182
    for i in range(len(cate_urls)):
        cate_url = cate_urls.iloc[i]["cate_url"]
        driver.get(cate_url)
        
        # Wait for page load and handle overlays
        wait_for_page_load(driver)

        while 1:
            # if t < ignore_i:
            #     print(f"Skipping category {i} because it's less than {ignore_i}")
            #     t += 1
            #     continue
            time.sleep(5)
            data1 = {
                "product_url": [],
                "product_img": []
            }
            
            # Handle overlays before processing products
            handle_overlays(driver)

            if t < ignore_i:
                print(f"Skipping category {i} because it's less than {ignore_i}")
            else:
                for product in driver.find_elements(By.XPATH, "//ul[@id='products_grid']/li"):
                    try:
                        p_url = product.find_element(By.XPATH,".//div[@class='product images-container']//a").get_attribute("href")
                        p_img = product.find_element(By.XPATH,".//div[@class='product images-container']//a//img").get_attribute("src")
                        data1["product_url"].append(p_url)
                        data1["product_img"].append(p_img)
                    except Exception as e:
                        print(f"Error extracting product data: {e}")
                        continue

            try:
                next_page_btn = driver.find_element(By.XPATH, "//li[@title='Next']/a")
                if force_click_element(driver, next_page_btn):
                    print(f"Successfully clicked Next button for {cate_url} page {t}")
                    # Wait for next page to load and handle overlays
                    wait_for_page_load(driver)
                else:
                    print(f"Failed to click Next button for {cate_url} page {t}")
                    break
            except Exception as e:
                print(f"Error finding or clicking Next button: {e}")
                break

            pd.DataFrame(data1).to_csv(f"./data/product_urls_{cate_url.split('/')[-1]}_{t}.csv", index=False)
            t += 1


if __name__ == "__main__":
    main()