from selenium.webdriver.common.by import By

class PaymentPage:
    name_on_card = (By.XPATH, "//input[@name='name_on_card']")
    card_number = (By.XPATH, "//input[@name='card_number']")
    cvv = (By.XPATH, "//input[@name='cvc']")
    exp_month = (By.XPATH, "//input[@name='expiry_month']")
    exp_year = (By.XPATH, "//input[@name='expiry_year']")
    pay_button = (By.XPATH, "//button[@id='submit']")

    def __init__(self, driver):
        self.driver = driver

    def fill_payment_info(self,fname,number,cvv,exp_month,exp_year):
        self.driver.find_element(*self.name_on_card).send_keys(fname)
        self.driver.find_element(*self.card_number).send_keys(number)
        self.driver.find_element(*self.cvv).send_keys(cvv)
        self.driver.find_element(*self.exp_month).send_keys(exp_month)
        self.driver.find_element(*self.exp_year).send_keys(exp_year)
        self.driver.find_element(*self.pay_button).click()