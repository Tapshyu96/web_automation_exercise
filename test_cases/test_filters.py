import time

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from unicodedata import category

from pages.Cart_Page import CartPage
from pages.Filters import FiltersSection
from pages.Home_Page import HomePage
from pages.Product_Page import ProductPage
from utilities.read_properties import Read_config
from utilities.custom_logs import LogMaker

class TestFilters:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()

# --------------View Category Products-------------------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that categories are visible on left sidebar
# 4. Click on 'Women' category
# 5. Click on any category link under 'Women' category, for example: Dress
# 6. Verify that category page is displayed and confirm text 'WOMEN - TOPS PRODUCTS'
# 7. On left sidebar, click on any sub-category link of 'Men' category
# 8. Verify that user is navigated to that category page
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_to_check_category(self,setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        time.sleep(2)
        self.logger.info("********Home Page is displayed********************")
        self.home = HomePage(self.driver)
        self.product = ProductPage(self.driver)
        self.filter = FiltersSection(self.driver)
        self.driver.execute_script("window.scrollTo(0, 200);")
        self.logger.info("********Category is displayed********************")
        for i in range(2):
            assert self.driver.find_element(By.XPATH,"//div[contains(@class,'category-products')]").is_displayed()
            main_category, subcategory, header = self.filter.category_check(i)
            expected_header = f"{main_category} - {subcategory} PRODUCTS"
            time.sleep(2)
            print(f"Expected Category Tittle: {expected_header.upper()}, Actual Category Title: {header.upper()}" )
            assert expected_header.upper() == header.upper()


#-----------------View & Cart Brand Products--------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Click on 'Products' button
# 4. Verify that Brands are visible on left sidebar
# 5. Click on any brand name
# 6. Verify that user is navigated to brand page and brand products are displayed
# 7. On left sidebar, click on any other brand link
# 8. Verify that user is navigated to that brand page and can see products
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_to_check_brand_filter(self,setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        time.sleep(2)
        self.logger.info("********Home Page is displayed********************")
        self.home = HomePage(self.driver)
        self.home.home_page('Products')
        self.logger.info("********Products Page is displayed********************")
        self.filter = FiltersSection(self.driver)
        self.driver.execute_script("window.scrollTo(0, 200);")
        self.logger.info("********Brand Filters is displayed********************")
        for i in range(2):
            assert self.driver.find_element(By.XPATH,"//div[contains(@class,'brands_products')]").is_displayed()
            brand_name, header = self.filter.brand_check(i)
            self.logger.info(f"********{brand_name.upper()} Brand is selected********************")
            expected_header = f"BRAND - {brand_name} PRODUCTS"
            if i == 0:
                assert self.driver.current_url == f"https://automationexercise.com/brand_products/{brand_name}"
            else:
                assert self.driver.current_url == f"https://automationexercise.com/brand_products/{brand_name.upper()}"
            assert expected_header.upper() == header.upper()

