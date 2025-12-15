import time
from asyncio import exceptions

from allure_pytest.plugin import select_by_testcase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class FiltersSection:

    # category = (By.XPATH,"//div[contains(@class,'category-products')]")
    category = (By.XPATH, "//h4[contains(@class,'panel-title')]//a")
    expand_icon = (By.XPATH, "//span[contains(@class,'badge pull-right')]")
    sub_category = (By.XPATH, "//div[@id='Women']//div//ul//li")

    product_header = (By.XPATH, "//h2[@class='title text-center']")

    brand = (By.XPATH, "//div[contains(@class,'brands_products')]")
    brand_items = (By.XPATH, "//div[contains(@class,'brands_products')]//ul//li//a")

    def __init__(self, driver):
        self.driver = driver

    def category_check(self,cat):
        c = self.driver.find_elements(*self.category)
        cat_name = c[cat].text.strip().capitalize()
        e = self.driver.find_elements(*self.expand_icon)
        e[cat].click()
        time.sleep(2)
        se = self.driver.find_elements(By.XPATH, f"//div[@id='{cat_name}']//div//ul//li//a")
        sub_cat_name = se[cat].text.strip()
        se[cat].click()
        time.sleep(2)
        header = self.driver.find_element(*self.product_header).text
        return cat_name, sub_cat_name, header

    def brand_check(self,brand):
        bi = self.driver.find_elements(*self.brand_items)
        br_name = bi[brand].text
        brand_name = br_name.splitlines()[-1].strip().capitalize()
        bi[brand].click()
        header = self.driver.find_element(*self.product_header).text.strip()
        return brand_name,header
