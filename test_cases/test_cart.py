import time

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from pages.Cart_Page import CartPage
from pages.Home_Page import HomePage
from pages.Product_Page import ProductPage
from utilities.read_properties import Read_config
from utilities.custom_logs import LogMaker

class TestCart:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()

# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click 'Products' button
# 5. Hover over first product and click 'Add to cart'
# 6. Click 'Continue Shopping' button
# 7. Hover over second product and click 'Add to cart'
# 8. Click 'View Cart' button
# 9. Verify both products are added to Cart
# 10. Verify their prices, quantity and total price
    @pytest.mark.sanity
    def test_add_product_to_cart(self,setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        time.sleep(2)
        self.logger.info("********Home Page is displayed********************")
        self.home = HomePage(self.driver)
        self.home.home_page('Products')
        self.logger.info("********Products Page is displayed********************")
        self.product_action = ProductPage(self.driver)
        items_price = []
        items_name = []
        self.logger.info("********Products are getting added to cart********************")
        for i in range(2):
            item_price = self.product_action.get_item_price_from_product_page(i)
            items_price.append(item_price)
            get_item_name = self.product_action.add_product_to_cart(i)
            items_name.append(get_item_name)
            alert_box = self.driver.find_element(By.XPATH, "//div[@class='modal-content']")
            time.sleep(2)
            assert alert_box.is_displayed()
            assert self.driver.find_element(By.XPATH,
                                            "//div[@class='modal-header']//child::h4").text.lower() == 'added!'

            if i == 0:
                self.driver.find_element(By.XPATH,
                                         "//div[@class='modal-footer']//child::button[text()='Continue Shopping']").click()
                time.sleep(2)

            if i == 1:
                self.driver.find_element(By.XPATH, "//div[@class='modal-body']//child::u[text()='View Cart']").click()
                time.sleep(5)
            self.logger.info(f"********{items_name} having {items_price} price are added to cart********************")

        assert self.driver.find_element(By.XPATH,"//table[@class='table table-condensed']").is_displayed()
        item_count_in_cart = len(self.driver.find_elements(By.XPATH, "//table[@id='cart_info_table']/tbody/tr"))
        assert item_count_in_cart == 2

        # ---Check the selected product added in cart or Not----
        self.logger.info("********Cart Page is Displayed********************")
        for i in range(2):
            item_details = self.product_action.get_item_details_from_cart_page(i)
            cart_values = item_details["items"][0]  # first product row
            found = False

            for value in items_name:
                if value in cart_values:
                    print(f"{value} found in cart")
                    self.logger.info(f"********{value} item found in cart********************")
                    found = True
                    assert True

                    for value1 in items_price:
                        price = int(cart_values[1].replace("Rs. ", "").strip())
                        qty = int(cart_values[2])
                        total_price = int(cart_values[-1].replace("Rs. ", "").strip())

                        if value1 == price:
                            print(f"Item {value} price {value1} found in cart")
                            self.logger.info(f"********{value1} price of {value} found in cart********************")
                            found = True
                            assert True
                            assert total_price == qty * price
                            self.logger.info(f"********{total_price} price is correct and matched in cart********************")

                            break


            if not found:
                self.logger.info(f"********Item is not found or matched with cart items********************")
                assert False



# -----------------Verify Product quantity in Cart---------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click 'View Product' for any product on home page
# 5. Verify product detail is opened
# 6. Increase quantity to 4
# 7. Click 'Add to cart' button
# 8. Click 'View Cart' button
# 9. Verify that product is displayed in cart page with exact quantity
    @pytest.mark.sanity
    def test_verify_the_quantity_in_cart(self,setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.logger.info("********Home Page is displayed********************")
        time.sleep(2)
        self.home = HomePage(self.driver)
        self.home.home_page('Products')
        self.logger.info("********Products Page is displayed********************")
        self.product_action = ProductPage(self.driver)

        items_price = []
        items_name = []
        item_price = self.product_action.get_item_price_from_product_page(0)
        items_price.append(item_price)
        self.driver.execute_script("window.scrollTo(0, 300);")
        self.product_action.items()
        self.logger.info("********Products Details Page is displayed********************")

        assert self.driver.find_element(By.XPATH, "//div[@class='product-information']").is_displayed()
        items_name.append(self.driver.find_element(By.XPATH, "//div[@class='product-information']//h2").text)

        assert self.driver.find_element(By.XPATH, "//div[@class='product-information']//h2").text == "Blue Top"
        other_elements = self.driver.find_elements(By.XPATH, "//div[@class='product-information']//p")
        check_details_of_product = ['Category: Women > Tops', 'Availability: In Stock', 'Condition: New', 'Brand: Polo']
        for el in other_elements:
            assert el.text in check_details_of_product


        self.logger.info("********Change the Product Quantity********************")
        qty = self.product_action.quantity_change(4)
        self.driver.implicitly_wait(10)
        time.sleep(2)
        alert_box = self.driver.find_element(By.XPATH, "//div[@class='modal-content']")
        assert alert_box.is_displayed()
        self.driver.find_element(By.XPATH, "//div[@class='modal-body']//child::u[text()='View Cart']").click()
        time.sleep(2)
        item_details = self.product_action.get_item_details_from_cart_page(0)
        cart_values = item_details["items"][0]
        for value in items_name:
            if value in cart_values:
                print(f"{value} found in cart")
                self.logger.info(f"********{value} item found in cart********************")
                qty_from_cart = int(cart_values[2])
                if qty == qty_from_cart:
                    self.logger.info(f"********Quantity from product details {qty} matched with Quantity from Cart i.e.{qty_from_cart}********************")
                    assert True
                else:
                    assert False



# ------------Remove Products From Cart------------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Add products to cart
# 5. Click 'Cart' button
# 6. Verify that cart page is displayed
# 7. Click 'X' button corresponding to particular product
# 8. Verify that product is removed from the cart

    def test_remove_product_from_cart(self,setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.logger.info("********Home Page is displayed********************")
        time.sleep(2)
        self.home = HomePage(self.driver)
        self.product_action = ProductPage(self.driver)
        item_price = self.product_action.get_item_price_from_product_page(0)
        name = self.driver.find_elements(By.XPATH, "//div[@class='productinfo text-center']//p")
        item_name = name[0].text
        self.home.add_product_to_cart()
        time.sleep(2)
        self.logger.info("********Product Added Successfully in cart********************")
        alert_box = self.driver.find_element(By.XPATH, "//div[@class='modal-content']")
        time.sleep(2)
        assert alert_box.is_displayed()
        assert self.driver.find_element(By.XPATH,
                                        "//div[@class='modal-header']//child::h4").text.lower() == 'added!'
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.driver.find_element(By.XPATH,
                                 "//div[@class='modal-footer']//child::button[text()='Continue Shopping']").click()
        self.home.home_page('Cart')
        item_details = self.product_action.get_item_details_from_cart_page(0)
        cart_values = item_details["items"][0]
        assert len(cart_values) == 4
        if item_name in cart_values:
            self.logger.info(f"********{item_name} item found in cart********************")
            assert True
        else:
            self.logger.info(f"********{item_name} item not found in cart********************")
            assert False
        self.cart = CartPage(self.driver)
        self.cart.remove_product_from_cart(0)
        time.sleep(2)
        assert self.driver.find_element(By.XPATH, '//span[@id="empty_cart"]').is_displayed()








