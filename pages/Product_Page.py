import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.common.by import By

class ProductPage:
    # --------Web Elements aon products Page---------------
    items_in_product = (By.XPATH,"//div[@class='single-products']")
    items_view_button = (By.XPATH,"//div[@class='choose']//child::a[text()='View Product']")
    item_information = (By.XPATH,"//div[@class='product-information']//*")
    search_product = (By.XPATH,"//input[@id='search_product']")
    search_icon = (By.XPATH,"//button[@id='submit_search']")
    items_price = (By.XPATH,"//div[@class='productinfo text-center']//h2")
    item_name = (By.XPATH,"//div[@class='overlay-content']//p")
    products = (By.XPATH,"//div[@class='productinfo text-center']//p")

    product_header = (By.XPATH,"//h2[@class='title text-center']")
    breadcrumb = (By.XPATH,"//div[@class='breadcrumbs']//li")

    # --------Web Elements after hover on single product---------------
    add_to_cart_button_on_hover = (By.XPATH,"//div[@class='overlay-content']//a[text()='Add to cart']")

    # --------Web Elements from Cart Page---------------
    cart_table = (By.XPATH,"//table[@id='cart_info_table']")
    cart_table_header = (By.XPATH,"//table[@id='cart_info_table']//tr[@class='cart_menu']")
    products_name_in_cart = (By.XPATH,"//table[@id='cart_info_table']/tbody/tr/td[@class='cart_description']/h4")
    products_price_in_cart = (By.XPATH,"//table[@id='cart_info_table']/tbody/tr/td[@class='cart_price']/p")
    product_quantity_in_cart = (By.XPATH,"//table[@id='cart_info_table']/tbody/tr/td[@class='cart_quantity']/button")
    product_total_price_in_cart = (By.XPATH,"//table[@id='cart_info_table']/tbody/tr/td[@class='cart_total']/p")


    # --------Web Elements from Product Details Page---------------
    quantity_in_product_details = (By.XPATH,"//input[@id='quantity']")
    add_to_cart_button_in_product_details = (By.XPATH,"//button[@class='btn btn-default cart']")


    def __init__(self, driver):
        self.driver = driver

    def items(self):
       items_view = self.driver.find_elements(*self.items_view_button)
       items_view[0].click()

    def serach_product(self, search_item):
        self.driver.find_element(*self.search_product).send_keys(search_item)
        self.driver.find_element(*self.search_icon).click()

    def add_product_to_cart(self,product_count):
        actions = ActionChains(self.driver)
        items_name = self.driver.find_elements(*self.item_name)
        items_view = self.driver.find_elements(*self.items_in_product)
        self.driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)
        actions.move_to_element(items_view[product_count]).perform()
        time.sleep(2)
        add_cart_buttons  = self.driver.find_elements(*self.add_to_cart_button_on_hover)
        actions.move_to_element(add_cart_buttons[product_count]).click().perform()
        item_name = items_name[product_count].text
        return item_name

    def get_item_price_from_product_page(self,product_count):
        item_price_in_string = self.driver.find_elements(*self.items_price)
        item_price_split = item_price_in_string[product_count].text.split(" ")
        actual_item_price = int(item_price_split[-1])
        return actual_item_price

    def get_item_details_from_cart_page(self,product_count):
        item_details_in_cart = {'items':[]}
        name = self.driver.find_elements(*self.products_name_in_cart)
        price = self.driver.find_elements(*self.products_price_in_cart)
        quantity = self.driver.find_elements(*self.product_quantity_in_cart)
        total_price = self.driver.find_elements(*self.product_total_price_in_cart)
        item_details_in_cart['items'].append(
            [name[product_count].text,
             price[product_count].text,
             quantity[product_count].text,
              total_price[product_count].text])
        return item_details_in_cart

    def quantity_change(self,quantity):
        self.driver.find_element(*self.quantity_in_product_details).clear()
        self.driver.find_element(*self.quantity_in_product_details).send_keys(quantity)
        self.driver.find_element(*self.add_to_cart_button_in_product_details).click()
        return quantity


    def category_header_check(self):
        header = self.driver.find_element(*self.product_header).text
        return header

    def get_products_info(self):
        p = self.driver.find_elements(*self.products)











