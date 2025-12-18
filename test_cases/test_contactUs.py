import time

from selenium.webdriver.common.by import By

from pages.ContactUs_Page import ContactUs
from pages.Home_Page import HomePage
from utilities.custom_logs import LogMaker
from utilities.read_properties import Read_config


class TestContactUs:
    Url = Read_config.get_url()
    logger = LogMaker.log_gen()

#Test Case 6: Contact Us Form
# 1. Launch browser
# 2. Navigate to url 'http://automationexercise.com'
# 3. Verify that home page is visible successfully
# 4. Click on 'Contact Us' button
# 5. Verify 'GET IN TOUCH' is visible
# 6. Enter name, email, subject and message
# 7. Upload file
# 8. Click 'Submit' button
# 9. Click OK button
# 10. Verify success message 'Success! Your details have been submitted successfully.' is visible
# 11. Click 'Home' button and verify that landed to home page successfully

    def test_contact_us(self, setup):
        self.driver = setup
        self.driver.get(self.Url)
        self.driver.maximize_window()
        self.logger.info("------Home Page Displayed------")
        assert self.driver.title == "Automation Exercise"
        assert self.driver.current_url == self.Url

        self.home = HomePage(self.driver)
        self.home.home_page("Contact us")
        time.sleep(3)
        assert self.driver.find_element(By.XPATH,"//h2[text()='Get In Touch']").is_displayed()
        file_for_contact = 'test_data/sample_file.txt'
        self.logger.info("------Contact Us Page Displayed------")
        self.contact_us = ContactUs(self.driver)
        self.contact_us.send_contact_info("Admin","Admin@123.com",
                                          "Administration","Test Message",
                                          file_for_contact)
        time.sleep(2)
        self.driver.switch_to.alert.accept()
        assert self.driver.find_element(By.XPATH,"//div[contains(@class,'success')]").is_displayed()
        assert self.driver.find_element(By.XPATH,"//div[contains(@class,'success')]").text == 'Success! Your details have been submitted successfully.'
        assert self.driver.find_element(By.XPATH,"//a[contains(@class,'success')]").is_displayed()
        self.driver.find_element(By.XPATH, "//a[contains(@class,'success')]").click()
        assert self.driver.title == "Automation Exercise"
        assert self.driver.current_url == self.Url