from selenium.webdriver.common.by import By

class Login:
    login_header = (By.XPATH,"//a[text()=' Signup / Login']")
    login_email = (By.XPATH,"//input[@data-qa='login-email']")
    login_password = (By.XPATH,"//input[@data-qa='login-password']")
    login_button = (By.XPATH,"//button[@data-qa='login-button']")
    logout_button = (By.XPATH,"//a[text()=' Logout']")


    def __init__(self, driver):
        self.driver = driver

    def go_to_login_page(self):
       self.driver.find_element(*self.login_header).click()

    def add_username(self, username):
        self.driver.find_element(*self.login_email).clear()
        self.driver.find_element(*self.login_email).send_keys(username)

    def add_password(self, password):
        self.driver.find_element(*self.login_password).clear()
        self.driver.find_element(*self.login_password).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def click_logout(self):
        self.driver.find_element(*self.logout_button).click()