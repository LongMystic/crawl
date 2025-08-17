import scrapy
import pandas as pd
from scrapy_selenium import SeleniumRequest

parent = []


class Second_Level_Spider(scrapy.Spider):
    name = "third_level"
    allowed_domains = ["banhkinhdo.com.vn"]
    start_urls = ["https://banhkinhdo.com.vn/danh-muc-san-pham/banh-afc-keo-choco/"]

    def start_requests(self):
        product_list = pd.read_csv("second_level.csv")
        for url in product_list["product_url"]:
            yield SeleniumRequest(
                url=f"{url}", callback=self.parse, meta={'product_url': url},
                wait_time=20,  # Increased wait time for images to load
                wait_until=lambda driver: (
                    driver.execute_script("return document.readyState") == "complete" and
                    self._wait_for_real_images(driver)
                )
            )
    
    def _wait_for_real_images(self, driver):
        """Wait for actual product images to load in the flickity-slider"""
        try:
            # Wait specifically for the flickity-slider to be present
            flickity_slider = driver.find_elements("css selector", "div.flickity-slider")
            if not flickity_slider:
                return False
                
            # Wait for images or links within the flickity-slider
            slider_images = driver.find_elements("css selector", "div.flickity-slider img")
            slider_links = driver.find_elements("css selector", "div.flickity-slider a")
            
            # Check if we have at least one real image or link (not placeholder)
            real_elements = []
            
            # Check images in slider
            for img in slider_images:
                src = img.get_attribute("src")
                if (src and 
                    not src.startswith("data:") and 
                    not "svg" in src.lower()):
                    real_elements.append(img)
                    
            # Check links in slider
            for link in slider_links:
                href = link.get_attribute("href")
                if (href and 
                    not href.startswith("data:") and 
                    not "svg" in href.lower()):
                    real_elements.append(link)
                    
            # If we don't have real elements yet, wait a bit more and check again
            if len(real_elements) == 0:
                import time
                time.sleep(3)  # Wait 3 more seconds
                
                # Check again
                slider_images = driver.find_elements("css selector", "div.flickity-slider img")
                slider_links = driver.find_elements("css selector", "div.flickity-slider a")
                
                for img in slider_images:
                    src = img.get_attribute("src")
                    if (src and 
                        not src.startswith("data:") and 
                        not "svg" in src.lower()):
                        real_elements.append(img)
                        
                for link in slider_links:
                    href = link.get_attribute("href")
                    if (href and 
                        not href.startswith("data:") and 
                        not "svg" in href.lower()):
                        real_elements.append(link)
                    
            return len(real_elements) > 0
        except Exception as e:
            return False
    
    def _is_website_element(self, image_url):
        """Check if an image is a common website element (logo, header, etc.)"""
        if not image_url:
            return True
            
        # Convert to lowercase for easier matching
        url_lower = image_url.lower()
        
        # Common website element patterns
        website_patterns = [
            'logo', 'header', 'banner', 'nav', 'navigation', 'menu',
            'footer', 'icon', 'favicon', 'social', 'facebook', 'twitter',
            'instagram', 'youtube', 'linkedin', 'pinterest',
            'wp-content/uploads/2020/07/logo',  # Specific to this website
            'wp-content/uploads/2020/07/logo-1.png',  # Exact logo URL
            'wp-content/themes', 'wp-content/plugins',
            'admin', 'wp-admin', 'wp-includes'
        ]
        
        # Check if URL contains any website element patterns
        for pattern in website_patterns:
            if pattern in url_lower:
                return True
                
        # Check for common image dimensions that are typically logos/icons
        # This would require additional logic if we want to check image dimensions
        
        return False

    def parse(self, response):
        # Debug: Log response status and body length
        self.logger.info(f"Response status: {response.status}")
        self.logger.info(f"Response body length: {len(response.body)}")
        
        product_name = response.xpath("//h1[@class='product-title product_title entry-title']/text()").get()
        product_name = str(product_name).strip()
        
        # Try multiple XPath selectors for product images
        product_image = None
        
        # Method 1: Try the original selector (product gallery) - flickity-slider links
        product_image = response.xpath("//div[@class='flickity-slider']//a/@href").get()
        
        # Method 2: Try alternative selectors if first one fails - flickity-slider images
        if not product_image:
            product_image = response.xpath("//div[@class='flickity-slider']//img/@src").get()
        
        # Filter out placeholder SVG images and data URLs
        if product_image and (product_image.startswith('data:image/svg+xml') or 
                             'svg' in product_image.lower() or
                             product_image.startswith('data:')):
            product_image = None
            
        # If we still don't have a real image, try to find non-placeholder images in flickity-slider only
        if not product_image or product_image.startswith('data:'):
            # Get all images and links from flickity-slider only
            slider_images = response.xpath("//div[@class='flickity-slider']//img/@src").getall()
            slider_links = response.xpath("//div[@class='flickity-slider']//a/@href").getall()
            
            # Combine both lists and filter out placeholders
            all_slider_elements = slider_images + slider_links
            for element_src in all_slider_elements:
                if (element_src and 
                    not element_src.startswith('data:') and 
                    not 'svg' in element_src.lower()):
                    product_image = element_src
                    break
        
        # Clean up the image URL if found
        if product_image:
            # Remove any relative paths and ensure full URL
            if product_image.startswith('//'):
                product_image = 'https:' + product_image
            elif product_image.startswith('/'):
                product_image = 'https://banhkinhdo.com.vn' + product_image
        
        # Debug logging
        self.logger.info(f"Product: {product_name}")
        self.logger.info(f"Image found: {product_image}")
        
        # Additional debugging: Log what we found in flickity-slider
        if not product_image:
            self.logger.warning(f"No image found for product: {product_name}")
            # Log what's in the flickity-slider
            slider_images = response.xpath("//div[@class='flickity-slider']//img/@src").getall()
            slider_links = response.xpath("//div[@class='flickity-slider']//a/@href").getall()
            self.logger.info(f"Flickity slider images: {slider_images}")
            self.logger.info(f"Flickity slider links: {slider_links}")
            
            # Log the actual HTML content of the flickity-slider
            flickity_html = response.xpath("//div[@class='flickity-slider']").get()
            if flickity_html:
                self.logger.info(f"Flickity slider HTML: {flickity_html[:1000]}...")  # First 1000 chars
            else:
                self.logger.info("No flickity-slider div found")
                
            # Also check if there are any other image containers
            all_images = response.xpath("//img/@src").getall()
            self.logger.info(f"All images on page (first 10): {all_images[:10]}")
            
            # Check for any divs that might contain product images
            product_gallery_divs = response.xpath("//div[contains(@class, 'gallery') or contains(@class, 'product') or contains(@class, 'image')]")
            self.logger.info(f"Found {len(product_gallery_divs)} potential product gallery divs")
            for i, div in enumerate(product_gallery_divs[:3]):  # Show first 3
                div_class = div.xpath("@class").get()
                div_content = div.xpath(".").get()
                self.logger.info(f"Gallery div {i+1} class: {div_class}")
                self.logger.info(f"Gallery div {i+1} content preview: {div_content[:200] if div_content else 'None'}...")
        else:
            # Log successful image extraction
            self.logger.info(f"Successfully extracted image: {product_image}")
            
            # Also log what type of image it is
            if product_image.startswith('http'):
                self.logger.info("Image is a full HTTP URL")
            elif product_image.startswith('//'):
                self.logger.info("Image is a protocol-relative URL")
            elif product_image.startswith('/'):
                self.logger.info("Image is a relative path")
            else:
                self.logger.info(f"Image format: {product_image[:50]}...")
                
        # product_description = response.xpath("//div[@id='tab-description']/text()").get()
        product_description = response.xpath(
            "//div[@id='tab-description']//text()"
        ).getall()

        # clean up whitespace and join into one string
        product_description = " ".join([t.strip() for t in product_description if t.strip()])
        barcode = response.xpath("//span[@class='sku']/text()").get()
        if product_name is not None and product_name != 'None':
            yield {
                'product_name': product_name,
                'product_url': response.meta['product_url'],
                'product_image': product_image,
                'product_description': product_description,
                'barcode': barcode
            }
