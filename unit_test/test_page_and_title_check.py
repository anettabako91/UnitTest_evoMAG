import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class TestPageandTitleCheck(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.evomag.ro/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()

    def tearDown(self):
        self.driver.quit()

    def test_check_page(self):
        self.driver.find_element(By.CSS_SELECTOR, '.lbhead')

    def test_title(self):
        title = self.driver.title
        expected_text = 'evoMAG.ro - Electronice si electrocasnice la un pret bun'
        self.assertEqual(title, expected_text, "there is an error in the title")
        print(f'the title is <{title}> and it is correct')