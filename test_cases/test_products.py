import time

import pytest
from selenium.webdriver.common.by import By

from pages.Home_Page import HomePage
from pages.Product_Page import ProductPage
from utilities.read_properties import Read_config
from utilities.custom_logs import LogMaker

class TestProducts:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()

# ---------Verify All Products and product detail page-----
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Products' button
# 5. Verify user is navigated to ALL PRODUCTS page successfully
# 6. The products list is visible
# 7. Click on 'View Product' of first product
# 8. User is landed to product detail page
# 9. Verify that detail is visible: product name, category, price, availability, condition, brand
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_product_page(self, setup):
        self.logger.info("------Product Page Displayed------")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.homemenu = HomePage(self.driver)
        self.homemenu.home_page('Products')
        if self.driver.current_url == "https://automationexercise.com/products":
            assert True
            self.logger.info("********Product Page Displayed and All products displayed********************")
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
        else:
            self.logger.info("********Product Page not displayed********************")
            self.driver.close()
            assert False
        self.product = ProductPage(self.driver)
        self.product.items()
        assert self.driver.find_element(By.XPATH,"//div[@class='product-information']").is_displayed()
        self.logger.info("********Single Product Information is displayed********************")
        assert self.driver.find_element(By.XPATH, "//div[@class='product-information']//h2").text == "Blue Top"
        other_elements = self.driver.find_elements(By.XPATH,"//div[@class='product-information']//p")
        check_details_of_product = ['Category: Women > Tops','Availability: In Stock','Condition: New','Brand: Polo']
        for el in other_elements:
            assert el.text in check_details_of_product
        self.driver.quit()


#---------------Search Product----------------------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Products' button
# 5. Verify user is navigated to ALL PRODUCTS page successfully
# 6. Enter product name in search input and click search button
# 7. Verify 'SEARCHED PRODUCTS' is visible
# 8. Verify all the products related to search are visible
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_search_product(self,setup):
        self.logger.info("------Product Page Displayed------")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.homemenu = HomePage(self.driver)
        self.homemenu.home_page('Products')
        if self.driver.current_url == "https://automationexercise.com/products":
            assert True
            self.logger.info("********Product Page Displayed and All products displayed********************")
            self.driver.execute_script("window.scrollTo(0, 50);")
            time.sleep(2)
        else:
            self.logger.info("********Product Page not displayed********************")
            self.driver.close()
            assert False
        self.product = ProductPage(self.driver)
        search_keyword = 'Top'
        self.logger.info(f"********Searching the {search_keyword}********************")
        self.product.serach_product(search_keyword)
        searched_items = self.driver.find_elements(By.XPATH,"//div[@class='productinfo text-center']//p")
        for items in searched_items:
            self.logger.info(f"********Result Found {items.text}********************")
            item_names = items.text.strip()
            if item_names:
                print("Checking Item Name", item_names)
                assert search_keyword.lower() in item_names.lower()
