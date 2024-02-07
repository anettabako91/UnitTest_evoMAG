import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class TestSearch(unittest.TestCase):
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input.sn-suggest-input')
    SEARCH_INPUT_XPATH = (By.XPATH, '//input[@placeholder="ce cauti astazi?"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '.submit-search')
    SEARCH_BUTTON_XPATH = (By.XPATH, '//input[@class="submit-search"]')
    PRODUCT_LIST_CONTAINER = (By.CSS_SELECTOR, "div.product_grid")
    PRODUCTS_SELECTOR = (By.CSS_SELECTOR, ".npi_name")
    PRODUCT_LIST_CONTAINER_XPATH = (By.XPATH, '//div[@class="product_grid"]')
    PRODUCTS_SELECTOR_XPATH = (By.XPATH,'//div[@class="npi_name"]')
    ERROR_MESSAGE_NO_PRODUCT = (By.CSS_SELECTOR, '.noResults')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.evomag.ro/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()

    def tearDown(self):
        self.driver.quit()

    def test_searching_products(self):
        self.search_product_CSS('Smartwatch Huawei')
        product_list_container = self.driver.find_element(*self.PRODUCT_LIST_CONTAINER)  # the grid with all products found
        products = product_list_container.find_elements(*self.PRODUCTS_SELECTOR)  # the name of the products found - a list of them
        print(f'we found {len(products)} products')  # print the lenght of the products list
        assert len(products) >= 10, f'the search resulted in less than 10 products '  # if the lenght is greater than 10, it means that the search resulted in more than 10 products
        print('test ok, we found more than 10 products')


    def test_searching_products_XPATH(self):
        self.search_product_XPATH('lego')
        time.sleep(2)
        product_list_container = self.driver.find_element(*self.PRODUCT_LIST_CONTAINER_XPATH)  # the grid with all products found
        products = product_list_container.find_elements(*self.PRODUCTS_SELECTOR_XPATH)  # the name of the products found - a list of them
        print(f'we found {len(products)} products')  # print the lenght of the products list
        assert len( products) >= 10, f'the search resulted in less than 10 products '  # if the lenght is greater than 10, it means that the search resulted in more than 10 products
        print('test ok, we found more than 10 products')


    def test_no_result_found(self):
        self.search_product_CSS('trandafir')
        expected_error_message = 'CRITERIILE DE FILTRARE SELECTATE DE DUMNEAVOASTRA NU AU RETURNAT NICI UN REZULTAT!'
        actual_error_message = self.driver.find_element(*self.ERROR_MESSAGE_NO_PRODUCT).text
        self.assertEqual(expected_error_message,actual_error_message,'there is an error in the actual error message. the expected message does not correspond to the actual message ')



    def search_product_CSS(self, searched_item):
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(searched_item)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def search_product_XPATH(self, searched_item):
        self.driver.find_element(*self.SEARCH_INPUT_XPATH).send_keys(searched_item)
        self.driver.find_element(*self.SEARCH_BUTTON_XPATH).click()