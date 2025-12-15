from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class RegisterPage:
    sign_name = (By.XPATH,"//input[@data-qa='signup-name']")
    sign_email = (By.XPATH,"//input[@data-qa='signup-email']")
    sign_button = (By.XPATH,"//button[@data-qa='signup-button']")

    #Account Information
    title = (By.XPATH,"//input[@id='id_gender1']")
    password = (By.XPATH,"//input[@id='password']")
    dob_days = (By.XPATH,"//select[@id='days']/option[text()='22']")
    dob_months = (By.XPATH, "//select[@id='months']/option[text()='June']")
    dob_years = (By.XPATH, "//select[@id='years']/option[text()='1996']")
    newsletter = (By.XPATH,"//input[@id='newsletter']")
    options = (By.XPATH,"//input[@id='optin']")

    #Address Information
    firstname = (By.XPATH,"//input[@id='first_name']")
    lastname = (By.XPATH,"//input[@id='last_name']")
    company = (By.XPATH,"//input[@id='company']")
    address = (By.XPATH,"//input[@id='address1']")
    country = (By.XPATH,"//select[@id='country']/option[text()='India']")
    state = (By.XPATH,"//input[@id='state']")
    city = (By.XPATH,"//input[@id='city']")
    zipcode = (By.XPATH,"//input[@id='zipcode']")
    mobile_number = (By.XPATH,"//input[@id='mobile_number']")
    create_account_button = (By.XPATH,"//button[@data-qa='create-account']")

    continue_button = (By.XPATH,"//a[text()='Continue']")
    def __init__(self, driver):
        self.driver = driver

    def fill_initial_information(self,username,password):
        self.driver.find_element(*self.sign_name).clear()
        self.driver.find_element(*self.sign_name).send_keys(username)
        self.driver.find_element(*self.sign_email).send_keys(password)
        self.driver.find_element(*self.sign_button).click()

    def fill_account_information(self,password1):
        self.driver.find_element(*self.title).click()
        self.driver.find_element(*self.password).send_keys(password1)
        self.driver.find_element(*self.dob_days).click()
        self.driver.find_element(*self.dob_months).click()
        self.driver.find_element(*self.dob_years).click()
        self.driver.find_element(*self.newsletter).click()
        self.driver.find_element(*self.options).click()

    def fill_address_information(self,f_name,l_name,address,state,city,zipcode,mob_no):
        self.driver.execute_script("window.scrollTo(0, 300);")
        self.driver.find_element(*self.firstname).send_keys(f_name)
        self.driver.find_element(*self.lastname).send_keys(l_name)
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.country).click()
        self.driver.find_element(*self.state).send_keys(state)
        self.driver.find_element(*self.city).send_keys(city)
        self.driver.find_element(*self.zipcode).send_keys(zipcode)
        self.driver.find_element(*self.mobile_number).send_keys(mob_no)
        self.driver.find_element(*self.create_account_button).click()

    def continue_register_user(self):
        self.driver.find_element(*self.continue_button).click()


