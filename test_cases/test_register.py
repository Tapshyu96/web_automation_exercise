import datetime
import random
import string
from operator import truediv

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.Login_Page import Login
from pages.Register_Page import RegisterPage
from utilities.custom_logs import LogMaker
from utilities.read_properties import Read_config
from datetime import datetime

class Test02Register:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()


# --------------------Register User and delete user-------------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Signup / Login' button
# 5. Verify 'New User Signup!' is visible
# 6. Enter name and email address
# 7. Click 'Signup' button
# 8. Verify that 'ENTER ACCOUNT INFORMATION' is visible
# 9. Fill details: Title, Name, Email, Password, Date of birth
# 10. Select checkbox 'Sign up for our newsletter!'
# 11. Select checkbox 'Receive special offers from our partners!'
# 12. Fill details: First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number
# 13. Click 'Create Account button'
# 14. Verify that 'ACCOUNT CREATED!' is visible
# 15. Click 'Continue' button
# 16. Verify that 'Logged in as username' is visible
# 17. Click 'Delete Account' button
# 18. Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button
#--------------------------------------------------------------------------------------------------
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_register_page_title(self, setup):
        self.logger.info("*********Register Page is displayed ********************")
        self.driver = setup

        try:
            self.driver.get(self.Url)
            self.driver.maximize_window()
            self.loObject = Login(self.driver)
            self.loObject.go_to_login_page()

            actual_title = self.driver.title
            expected_title = "Automation Exercise - Signup / Login"

            assert actual_title == expected_title

        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = f".\\screenshots\\test_register_page_title_{timestamp}.png"
            self.driver.save_screenshot(path)
            raise e

        finally:
            self.driver.close()

    @pytest.mark.sanity
    @pytest.mark.regression
    @pytest.mark.register
    def test_register_user(self,setup):
        self.logger.info("*********Register Page is displayed********************")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.loObject = Login(self.driver)
        self.loObject.go_to_login_page()
        self.reg = RegisterPage(self.driver)
        email = generate_email()
        username = generate_username()
        self.reg.fill_initial_information(username,email)
        self.reg.fill_account_information('Admin@123')
        self.reg.fill_address_information('FirstName','LastName','Address','Maharashtra'
                                          ,'Nagpur','440005','986094861')
        account_created_text = self.driver.find_element(By.XPATH,"//b[text()='Account Created!']").text
        if account_created_text == 'ACCOUNT CREATED!':
            assert True
            Account_Message = self.driver.find_element(By.XPATH,"//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'Congratulations')]").text
            Account_Message2 = self.driver.find_element(By.XPATH,
                                                       "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'advantage')]").text
            self.logger.info(account_created_text)
            self.logger.info(Account_Message)
            self.logger.info(Account_Message2)
            self.reg.continue_register_user()
            loginUserName = self.driver.find_element(By.XPATH,f"//a[contains(text(),'Logged')]//child::b[text()='{username}']")
            if loginUserName.is_displayed():
                assert True
                self.driver.find_element(By.XPATH,"//a[contains(text(),'Delete')]").click()
                account_deleted_text = self.driver.find_element(By.XPATH, "//b[text()='Account Deleted!']").text
                if account_deleted_text == 'ACCOUNT DELETED!':
                    assert True
                    Account_Message3 = self.driver.find_element(By.XPATH,
                                                               "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'deleted')]").text
                    Account_Message4 = self.driver.find_element(By.XPATH,
                                                                "//div[@class='col-sm-9 col-sm-offset-1']/p[contains(text(),'advantage')]").text
                    self.logger.info(account_deleted_text)
                    self.logger.info(Account_Message3)
                    self.logger.info(Account_Message4)
                    self.reg.continue_register_user()
                    self.driver.close()
            else:
                self.driver.save_screenshot(".\\screenshots\\test_register_user.png")
                self.logger.info("*********User created but Not logged in Successfully********************")
                self.driver.close()
                assert False
        else:
            self.driver.save_screenshot(".\\screenshots\\test_register_user.png")
            self.logger.info("*********User Not Created Successfully********************")
            self.driver.close()
            assert False

# ------------------------------------------------------
# Register User with existing email--------------------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Signup / Login' button
# 5. Verify 'New User Signup!' is visible
# 6. Enter name and already registered email address
# 7. Click 'Signup' button
# 8. Verify error 'Email Address already exist!' is visible
    @pytest.mark.regression
    def test_register_user_with_existing_email(self,setup):
        self.logger.info("*********Register User Page is displayed********************")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.loObject = Login(self.driver)
        self.loObject.go_to_login_page()
        self.reg = RegisterPage(self.driver)
        self.reg.fill_initial_information('Tapshyu Ganvir','tapshyuganvir@gmail.com')
        validation_message = self.driver.find_element(By.XPATH,"//p[text()='Email Address already exist!']").text
        if validation_message == 'Email Address already exist!':
            self.logger.info(validation_message)
            assert True
            self.driver.close()
        else:
            self.driver.save_screenshot(".\\screenshots\\test_register_user_with_existing_email.png")
            self.logger.info("*********Email Id present in system but still user is able to create new account********************")
            self.driver.close()
            assert False

def generate_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{random.choice(domains)}"

def generate_username():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{name}"