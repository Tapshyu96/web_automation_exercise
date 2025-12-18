import random
import string

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from pages.Cart_Page import CartPage
from pages.Home_Page import HomePage
from pages.Login_Page import Login
from pages.PaymentPage import PaymentPage
from pages.Register_Page import RegisterPage
from utilities.custom_logs import LogMaker
from utilities.read_properties import Read_config


class TestOrders:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()
    username = Read_config.get_username()
    password = Read_config.get_password()

#--------------Place Order: Register while Checkout--------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Add products to cart
# 5. Click 'Cart' button
# 6. Verify that cart page is displayed
# 7. Click Proceed To Checkout
# 8. Click 'Register / Login' button
# 9. Fill all details in Signup and create account
# 10. Verify 'ACCOUNT CREATED!' and click 'Continue' button
# 11. Verify ' Logged in as username' at top
# 12.Click 'Cart' button
# 13. Click 'Proceed To Checkout' button
# 14. Verify Address Details and Review Your Order
# 15. Enter description in comment text area and click 'Place Order'
# 16. Enter payment details: Name on Card, Card Number, CVC, Expiration date
# 17. Click 'Pay and Confirm Order' button
# 18. Verify success message 'Your order has been placed successfully!'
# 19. Click 'Delete Account' button
# 20. Verify 'ACCOUNT DELETED!' and click 'Continue' button

    def test_register_while_checkout(self,setup):
      self.driver = setup
      self.driver.get(self.Url)
      self.driver.maximize_window()
      self.logger.info("------Home Page Displayed------")
      assert self.driver.title == "Automation Exercise"
      assert self.driver.current_url == self.Url

      self.home = HomePage(self.driver)
      self.home.add_product_to_cart()
      self.logger.info("------First Product added in cart------")
      time.sleep(2)
      alert_box = self.driver.find_element(By.XPATH, "//div[@class='modal-content']")
      assert alert_box.is_displayed()
      self.driver.find_element(By.XPATH, "//div[@class='modal-footer']//child::button[text()='Continue Shopping']").click()
      time.sleep(2)
      self.logger.info("------Cart page is displayed------")
      self.home.home_page("Cart")

      time.sleep(2)
      assert self.driver.current_url == "https://automationexercise.com/view_cart"
      assert self.driver.title == "Automation Exercise - Checkout"

      self.cart = CartPage(self.driver)
      self.cart.proceed_to_checkout()
      time.sleep(2)

      assert self.driver.find_element(By.XPATH, "//div[@class='modal-content']").is_displayed()
      time.sleep(2)
      self.logger.info("------Now user is getting created------")
      self.cart.register_login_click()
      time.sleep(2)

      self.register = RegisterPage(self.driver)
      username = generate_username()
      password = generate_email()
      self.register.fill_initial_information(username,password)
      self.register.fill_account_information(password)
      self.register.fill_address_information("ABCD","DEFG","HIJK",
                                             "LMOP","QRST","445566",
                                             "9876543210")
      account_created_text = self.driver.find_element(By.XPATH, "//b[text()='Account Created!']").text
      if account_created_text == 'ACCOUNT CREATED!':
          assert True
          Account_Message = self.driver.find_element(By.XPATH,
                                                     "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'Congratulations')]").text
          Account_Message2 = self.driver.find_element(By.XPATH,
                                                      "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'advantage')]").text
          self.logger.info(account_created_text)
          self.logger.info(Account_Message)
          self.logger.info(Account_Message2)
          self.register.continue_register_user()
          loginUserName = self.driver.find_element(By.XPATH,
                                                   f"//a[contains(text(),'Logged')]//child::b[text()='{username}']")
          if loginUserName.is_displayed():
              assert True
          else:
              assert False
      else:
          assert False

      self.home.home_page("Cart")
      self.cart.proceed_to_checkout()
      time.sleep(2)
      self.logger.info("------Checkout page is displayed------")
      self.cart.check_address_info()
      self.driver.execute_script("window.scrollTo(0, 500);")
      self.cart.add_description("Good Product")
      self.cart.place_order_from_cart()
      self.logger.info("------Payment page is displayed------")
      self.payment = PaymentPage(self.driver)
      self.payment.fill_payment_info("Admin User","9876987665433210",
                                     "654","12","2099")
      #assert self.driver.find_element(By.XPATH,"//div[@id='success_message']").is_displayed()
      time.sleep(5)

      assert self.driver.find_element(By.XPATH,"//b[text()='Order Placed!']").text == "ORDER PLACED!"
      assert self.driver.find_element(By.XPATH,"//a[text()='Continue']").is_displayed()
      assert self.driver.find_element(By.XPATH,"//a[text()='Download Invoice']").is_displayed()
      self.logger.info("------Now user is getting deleted------")
      self.driver.find_element(By.XPATH, "//a[contains(text(),'Delete')]").click()
      time.sleep(2)
      account_deleted_text = self.driver.find_element(By.XPATH, "//b[text()='Account Deleted!']").text
      if account_deleted_text == 'ACCOUNT DELETED!':
          assert True
          self.logger.info(account_deleted_text)
      else:
          assert False


# -------------- Place Order: Register before Checkout------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click 'Signup / Login' button
# 5. Fill all details in Signup and create account
# 6. Verify 'ACCOUNT CREATED!' and click 'Continue' button
# 7. Verify ' Logged in as username' at top
# 8. Add products to cart
# 9. Click 'Cart' button
# 10. Verify that cart page is displayed
# 11. Click Proceed To Checkout
# 12. Verify Address Details and Review Your Order
# 13. Enter description in comment text area and click 'Place Order'
# 14. Enter payment details: Name on Card, Card Number, CVC, Expiration date
# 15. Click 'Pay and Confirm Order' button
# 16. Verify success message 'Your order has been placed successfully!'
# 17. Click 'Delete Account' button
# 18. Verify 'ACCOUNT DELETED!' and click 'Continue' button
    def test_register_before_checkout(self, setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.logger.info("------Home Page Displayed------")
        assert self.driver.title == "Automation Exercise"
        assert self.driver.current_url == self.Url
        time.sleep(2)
        self.home = HomePage(self.driver)
        self.home.home_page("Signup / Login")
        self.logger.info("------Login / Signup Page Displayed------")
        self.register = RegisterPage(self.driver)
        username = generate_username()
        password = generate_email()
        self.register.fill_initial_information(username, password)
        self.register.fill_account_information(password)
        self.register.fill_address_information("ABCD", "DEFG", "HIJK",
                                               "LMOP", "QRST", "445566",
                                               "9876543210")
        account_created_text = self.driver.find_element(By.XPATH, "//b[text()='Account Created!']").text
        if account_created_text == 'ACCOUNT CREATED!':
            assert True
            Account_Message = self.driver.find_element(By.XPATH,
                                                       "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'Congratulations')]").text
            Account_Message2 = self.driver.find_element(By.XPATH,
                                                        "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'advantage')]").text
            self.logger.info(account_created_text)
            self.logger.info(Account_Message)
            self.logger.info(Account_Message2)
            self.register.continue_register_user()
            loginUserName = self.driver.find_element(By.XPATH,
                                                     f"//a[contains(text(),'Logged')]//child::b[text()='{username}']")
            if loginUserName.is_displayed():
                assert True
            else:
                assert False
        else:
            assert False
        self.cart = CartPage(self.driver)
        self.home.add_product_to_cart()
        self.logger.info("------First Product added in cart------")
        time.sleep(2)
        alert_box = self.driver.find_element(By.XPATH, "//div[@class='modal-content']")
        assert alert_box.is_displayed()
        self.driver.find_element(By.XPATH,
                                 "//div[@class='modal-footer']//child::button[text()='Continue Shopping']").click()
        time.sleep(2)
        self.logger.info("------Cart page is displayed------")
        self.home.home_page("Cart")
        assert self.driver.current_url == "https://automationexercise.com/view_cart"
        time.sleep(2)

        self.cart.proceed_to_checkout()
        time.sleep(2)
        self.logger.info("------Checkout page is displayed------")
        self.cart.check_address_info()
        self.driver.execute_script("window.scrollTo(0, 500);")
        self.cart.add_description("Good Product")
        self.cart.place_order_from_cart()
        self.logger.info("------Payment page is displayed------")
        self.payment = PaymentPage(self.driver)
        self.payment.fill_payment_info("Admin User", "9876987665433210",
                                       "654", "12", "2099")
        #assert self.driver.find_element(By.XPATH, "//div[@id='success_message']").is_displayed()
        time.sleep(5)

        assert self.driver.find_element(By.XPATH, "//b[text()='Order Placed!']").text == "ORDER PLACED!"
        assert self.driver.find_element(By.XPATH, "//a[text()='Continue']").is_displayed()
        assert self.driver.find_element(By.XPATH, "//a[text()='Download Invoice']").is_displayed()
        self.logger.info("------Now user is getting deleted------")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Delete')]").click()
        time.sleep(2)
        account_deleted_text = self.driver.find_element(By.XPATH, "//b[text()='Account Deleted!']").text
        if account_deleted_text == 'ACCOUNT DELETED!':
            assert True
            self.logger.info(account_deleted_text)
        else:
            assert False

# --------------- Place Order: Login before Checkout
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click 'Signup / Login' button
# 5. Fill email, password and click 'Login' button
# 6. Verify 'Logged in as username' at top
# 7. Add products to cart
# 8. Click 'Cart' button
# 9. Verify that cart page is displayed
# 10. Click Proceed To Checkout
# 11. Verify Address Details and Review Your Order
# 12. Enter description in comment text area and click 'Place Order'
# 13. Enter payment details: Name on Card, Card Number, CVC, Expiration date
# 14. Click 'Pay and Confirm Order' button
# 15. Verify success message 'Your order has been placed successfully!'
    def test_login_befor_checkout(self,setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.logger.info("------Home Page Displayed------")
        assert self.driver.title == "Automation Exercise"
        assert self.driver.current_url == self.Url
        time.sleep(2)
        self.home = HomePage(self.driver)
        self.home.home_page("Signup / Login")
        self.logger.info("------Login / Signup Page Displayed------")
        self.login = Login(self.driver)
        self.login.add_username(self.username)
        self.login.add_password(self.password)
        self.login.click_login()
        actual_result = self.driver.find_element(By.XPATH, "//b[text()='Admin']").text
        expected_result = "Admin"
        if actual_result == expected_result:
            self.logger.info("********User Login Successfully********************")
            assert True
        else:
            self.logger.info("********User Login Failed********************")
            assert False
        self.cart = CartPage(self.driver)
        self.home.add_product_to_cart()
        self.logger.info("------First Product added in cart------")
        time.sleep(2)
        alert_box = self.driver.find_element(By.XPATH, "//div[@class='modal-content']")
        assert alert_box.is_displayed()
        self.driver.find_element(By.XPATH,
                                 "//div[@class='modal-footer']//child::button[text()='Continue Shopping']").click()
        time.sleep(2)
        self.logger.info("------Cart page is displayed------")
        self.home.home_page("Cart")
        assert self.driver.current_url == "https://automationexercise.com/view_cart"
        time.sleep(2)

        self.cart.proceed_to_checkout()
        time.sleep(2)
        self.logger.info("------Checkout page is displayed------")
        self.cart.check_address_info()
        self.driver.execute_script("window.scrollTo(0, 500);")
        self.cart.add_description("Good Product")
        self.cart.place_order_from_cart()
        self.logger.info("------Payment page is displayed------")
        self.payment = PaymentPage(self.driver)
        self.payment.fill_payment_info("Admin User", "9876987665433210",
                                       "654", "12", "2099")
        #assert self.driver.find_element(By.XPATH, "//div[@id='success_message']").is_displayed()
        time.sleep(5)

        assert self.driver.find_element(By.XPATH, "//b[text()='Order Placed!']").text == "ORDER PLACED!"
        assert self.driver.find_element(By.XPATH, "//a[text()='Continue']").is_displayed()
        assert self.driver.find_element(By.XPATH, "//a[text()='Download Invoice']").is_displayed()
        self.logger.info("------Now user is getting deleted------")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Delete')]").click()
        time.sleep(2)
        account_deleted_text = self.driver.find_element(By.XPATH, "//b[text()='Account Deleted!']").text
        if account_deleted_text == 'ACCOUNT DELETED!':
            assert True
            self.logger.info(account_deleted_text)
        else:
            assert False



def generate_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{random.choice(domains)}"

def generate_username():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{name}"