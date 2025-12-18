import os

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class ContactUs:

    #-------------Elements from Contact Us form------------
    name = (By.NAME, "name")
    email = (By.NAME, "email")
    subject = (By.NAME, "subject")
    message = (By.ID,"message")
    file = (By.NAME,"upload_file")
    submit = (By.NAME,"submit")



    def __init__(self,driver):
        self.driver = driver

    def send_contact_info(self,name,email,subject,message,file):
        project_root = os.getcwd()
        absolute_file_path = os.path.abspath(os.path.join(project_root, file))
        self.driver.find_element(*self.name).send_keys(name)
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.subject).send_keys(subject)
        self.driver.find_element(*self.message).send_keys(message)
        self.driver.find_element(*self.file).send_keys(absolute_file_path)
        self.driver.find_element(*self.submit).click()
