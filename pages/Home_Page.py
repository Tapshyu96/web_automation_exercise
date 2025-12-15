from asyncio import exceptions

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class HomePage:

    subscription_email = (By.XPATH,"//input[@id='susbscribe_email']")
    subscription_button = (By.XPATH,"//button[@id='subscribe']")
    add_to_cart = (By.XPATH,"//a[contains(@class,'add-to-cart')]")

    def __init__(self, driver):
        self.driver = driver


    def home_page(self,linktext):
        user_input_in_xpath = f"//a[normalize-space(text())='{linktext}']"
        try:
            self.driver.find_element(By.XPATH,user_input_in_xpath).click()
        except NoSuchElementException:
            print(f"No Element on web")


    def subscription_check(self,emai_for_subscription):
        self.driver.find_element(*self.subscription_email).send_keys(emai_for_subscription)
        self.driver.find_element(*self.subscription_button).click()

    def add_product_to_cart(self):
        self.driver.execute_script("window.scrollTo(0, 500);")
        product = self.driver.find_elements(*self.add_to_cart)
        product[0].click()

