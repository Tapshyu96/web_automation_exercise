import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.common.by import By

class CartPage:
    empty_cart_div = (By.XPATH, '//span[@id="empty_cart"]')
    remove_cart_item = (By.XPATH, "//table[@id='cart_info_table']/tbody/tr/td[@class='cart_delete']/a")

    proceed_to_checkout_button = (By.XPATH, "//a[text()='Proceed To Checkout']")

    #-------Elements of Checkout popup----------
    pop_box = (By.XPATH, "//div[@class='modal-content']")
    register_login_link = (By.XPATH, "//div[@class='modal-body']//child::p[@class='text-center']//a")
    register_login_text = (By.XPATH, "//div[@class='modal-body']//child::p[@class='text-center']")
    continue_on_cart_button = (By.XPATH, "//div[@class='modal-footer']//button[text()='Continue On Cart']")

    # -------Elements of Checkout Page----------
    check_headers_of_sections = (By.XPATH, "//div[@class='step-one']")
    delivery_address = (By.XPATH, "//ul[@id='address_delivery']//li")
    billing_address = (By.XPATH, "//ul[@id='address_invoice']//li")

    products_name_in_cart = (By.XPATH, "//table[@class='table table-condensed']/tbody/tr/td[@class='cart_description']/h4")
    products_price_in_cart = (By.XPATH, "//table[@class='table table-condensed']/tbody/tr/td[@class='cart_price']/p")
    product_quantity_in_cart = (By.XPATH, "//table[@class='table table-condensed']/tbody/tr/td[@class='cart_quantity']/button")
    product_total_price_in_cart = (By.XPATH, "//p[@class='cart_total_price']")

    add_description_area = (By.XPATH, "//div[@id='ordermsg']//textarea")
    place_order = (By.XPATH, "//a[text()='Place Order']")


    def __init__(self, driver):
        self.driver = driver

    def remove_product_from_cart(self,items):
        del_buttons = self.driver.find_elements(*self.remove_cart_item)
        del_buttons[items].click()

    def proceed_to_checkout(self):
        self.driver.find_element(*self.proceed_to_checkout_button).click()

    def register_login_click(self):
        self.driver.find_element(*self.register_login_link).click()

    def continue_on_cart_click(self):
        self.driver.find_element(*self.continue_on_cart_button).click()

    def check_address_info(self):
        del_add = self.driver.find_elements(*self.delivery_address)
        bil_add = self.driver.find_elements(*self.billing_address)

        for add1, add2 in zip(del_add[1:],bil_add[1:]):
            print(f"Checking that {add1.text} and {add2.text} are same or Not!")
            assert add1.text == add2.text
        return True

    def add_description(self,description):
        self.driver.find_element(*self.add_description_area).send_keys(description)

    def place_order_from_cart(self):
        self.driver.find_element(*self.place_order).click()