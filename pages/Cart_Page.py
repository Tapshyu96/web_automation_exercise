import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.common.by import By

class CartPage:
    empty_cart_div = (By.XPATH, '//span[@id="empty_cart"]')
    remove_cart_item = (By.XPATH, "//table[@id='cart_info_table']/tbody/tr/td[@class='cart_delete']/a")

    def __init__(self, driver):
        self.driver = driver

    def remove_product_from_cart(self,items):
        del_buttons = self.driver.find_elements(*self.remove_cart_item)
        del_buttons[items].click()
