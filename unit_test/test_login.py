import unittest
import time

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By


class TestLogin(unittest.TestCase):
    EMAIL_FIELD_SELECTOR = (By.XPATH, '//input[@name="LoginClientForm[Email]"]')
    PASSWORD_FIELD_SELECTOR = (By.XPATH, '//input[@id="LoginClientForm_Password"]')
    ERROR_MESSAGE_SELECTOR = (By.XPATH, '//div[@class="generic_error_message err1"]')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.evomag.ro/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        action = ActionChains(self.driver)
        self.driver.find_element(By.XPATH, '//div[contains(text(),"Login")]').click()
        self.driver.find_element(By.XPATH, '//a[@class="BtnLoginHead"]').click()
        self.driver.find_element(*self.EMAIL_FIELD_SELECTOR).send_keys('abds@gmail.com')
        action.send_keys(Keys.TAB).perform()
        action.send_keys('0745875412657')
        action.send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        error_message = self.driver.find_element(*self.ERROR_MESSAGE_SELECTOR).text.strip()
        expected_message = "Utilizatorul nu exista, va recomandam sa creati unul nou."
        self.assertEqual(error_message,expected_message, "the error message is not correct")
        print('the correct error message is returned')


    def test_login_wrong_format_email(self):
        action = ActionChains(self.driver)
        self.driver.find_element(By.XPATH, '//div[contains(text(),"Login")]').click()
        self.driver.find_element(By.XPATH, '//a[@class="BtnLoginHead"]').click()
        self.driver.find_element(*self.EMAIL_FIELD_SELECTOR).send_keys('email.com')
        action.send_keys(Keys.TAB).perform()
        action.send_keys('qwerrtyyui')
        action.send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        actual_error_message = self.driver.find_element(*self.ERROR_MESSAGE_SELECTOR).text.strip()
        expected_error_message = "Nu va puteti autentifica! Adresa de email introdusa este invalida!"
        self.assertEqual(actual_error_message,expected_error_message,"there is an error, the expected error message does not correspond to the actual error message")


