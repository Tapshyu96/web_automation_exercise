import time

import pytest
from selenium.webdriver.common.by import By

from pages.Home_Page import HomePage
from utilities.custom_logs import LogMaker
from utilities.read_properties import Read_config


class TestSubscription:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()
    username = Read_config.get_username()

#-------------------------------Verify Subscription in home page------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Scroll down to footer
# 5. Verify text 'SUBSCRIPTION'
# 6. Enter email address in input and click arrow button
# 7. Verify success message 'You have been successfully subscribed!' is visible
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_verify_subscription_on_home_page(self, setup):
        self.logger.info("------Home Page Displayed------")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        subscription_text = self.driver.find_element(By.XPATH,"//h2[text()='Subscription']").text
        self.logger.info(f"------{subscription_text} Displayed on Home Page------")

        assert subscription_text.lower() == 'subscription'

        self.home = HomePage(self.driver)
        self.home.subscription_check(self.username)
        success_message = 'You have been successfully subscribed!'
        success_message_element = self.driver.find_element(By.XPATH,"//div[@class='alert-success alert']").text

        assert success_message.lower() == success_message_element.lower()


# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click 'Cart' button
# 5. Scroll down to footer
# 6. Verify text 'SUBSCRIPTION'
# 7. Enter email address in input and click arrow button
# 8. Verify success message 'You have been successfully subscribed!' is visible
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_verify_subscription_on_cart_page(self, setup):
        self.logger.info("------Home Page Displayed------")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.home = HomePage(self.driver)
        self.home.home_page('Cart')
        self.logger.info("------Cart Page Displayed------")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        assert self.driver.current_url == "https://automationexercise.com/view_cart"
        assert self.driver.find_element(By.XPATH,"//ol[@class='breadcrumb']//li[text()='Shopping Cart']").is_displayed()

        subscription_text = self.driver.find_element(By.XPATH, "//h2[text()='Subscription']").text
        self.logger.info(f"------{subscription_text} Displayed on Home Page------")

        assert subscription_text.lower() == 'subscription'

        self.home.subscription_check(self.username)
        success_message = 'You have been successfully subscribed!'
        success_message_element = self.driver.find_element(By.XPATH, "//div[@class='alert-success alert']").text
        self.driver.implicitly_wait(2)

        assert success_message.lower() == success_message_element.lower()