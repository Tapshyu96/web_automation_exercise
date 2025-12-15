from typing import assert_type

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.Login_Page import Login
from utilities.read_properties import Read_config
from utilities.custom_logs import LogMaker

class Test01Login:
    Url = Read_config.get_url()
    username = Read_config.get_username()
    password = Read_config.get_password()
    invalid_username = Read_config.get_invalid_username()
    invalid_password = Read_config.get_invalid_password()
    logger = LogMaker.log_gen()

#---------------------------------------
#--------Verify the Page title----------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully and match the title
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_verify_page_title(self,setup):
        self.logger.info("*********test_verify_page_title********************")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        actual_title = self.driver.title
        expected_title = "Automation Exercise"
        if actual_title == expected_title:
            self.logger.info("*********Title Matched with Expected Title********************")
            assert True
            self.driver.close()
        else:
            self.driver.save_screenshot(".\\screenshots\\test_verify_page_title.png")
            self.logger.info("*********Title Not Matched with Expected Title********************")
            self.driver.close()
            assert False

#------------------------------------------------
#-----------Login User with correct email and password--------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Signup / Login' button
# 5. Verify 'Login to your account' is visible
# 6. Enter correct email address and password
# 7. Click 'login' button
# 8. Verify that 'Logged in as username' is visible
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_valid_login(self,setup):
        self.logger.info("*********Login with Valid Credentials********************")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.loObject = Login(self.driver)
        self.loObject.go_to_login_page()
        self.loObject.add_username(self.username)
        self.loObject.add_password(self.password)
        self.loObject.click_login()
        actual_result = self.driver.find_element(By.XPATH,"//b[text()='Admin']").text
        expected_result = "Admin"
        if actual_result == expected_result:
            self.logger.info("********User Login Successfully********************")
            assert True
            self.driver.close()
        else:
            self.logger.info("********User Login Failed********************")
            self.driver.save_screenshot(".\\screenshots\\test_valid_login.png")
            self.driver.close()
            assert False


#--------------------------------------------------------------------
#-------------Login User with incorrect email and password----------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Signup / Login' button
# 5. Verify 'Login to your account' is visible
# 6. Enter incorrect email address and password
# 7. Click 'login' button
# 8. Verify error 'Your email or password is incorrect!' is visible
    @pytest.mark.regression
    def test_invalid_login(self,setup):
        self.logger.info("********Login with Invalid Credentials********************")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.loObject = Login(self.driver)
        self.loObject.go_to_login_page()
        self.loObject.add_username(self.invalid_username)
        self.loObject.add_password(self.invalid_password)
        self.loObject.click_login()
        actual_result = self.driver.find_element(By.XPATH,"//p[text()='Your email or password is incorrect!']").text
        expected_result = "Your email or password is incorrect!"
        if actual_result == expected_result:
            self.logger.info("********User Not Login Successfully********************")
            assert True
            self.driver.close()
        else:
            self.logger.info("********User Login Successfully********************")
            self.driver.save_screenshot(".\\screenshots\\test_invalid_login.png")
            self.driver.close()
            assert False

#--------------------------------------------------------------------
#-------------Logout User----------
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Signup / Login' button
# 5. Verify 'Login to your account' is visible
# 6. Enter correct email address and password
# 7. Click 'login' button
# 8. Verify that 'Logged in as username' is visible
# 9. Click 'Logout' button
# 10. Verify that user is navigated to login page
    @pytest.mark.sanity
    @pytest.mark.regression
    def test_logout(self,setup):
        self.logger.info("********Logout User********************")
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.loObject = Login(self.driver)
        self.loObject.go_to_login_page()
        self.loObject.add_username(self.username)
        self.loObject.add_password(self.password)
        self.loObject.click_login()
        actual_result = self.driver.find_element(By.XPATH, "//b[text()='Admin']").text
        expected_result = "Admin"
        if actual_result == expected_result:
            self.logger.info("********User Login Successfully********************")
            assert True
            self.loObject.click_logout()
            if self.driver.current_url == "https://automationexercise.com/login":
                self.logger.info("********User Logout Successfully********************")
                assert True
                self.driver.close()
            else:
                self.logger.info("********User not Logout Successfully********************")
                self.driver.save_screenshot(".\\screenshots\\test_logout.png")
                self.driver.close()
                assert False
        else:
            self.logger.info("********User Login Failed********************")
            self.driver.save_screenshot(".\\screenshots\\test_logout.png")
            self.driver.close()
            assert False