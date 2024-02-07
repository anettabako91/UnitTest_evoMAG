import unittest
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

#this works only if searched products are still available

class TestCart(unittest.TestCase):
    SEARCH_INPUT_XPATH = (By.XPATH, '//input[@placeholder="ce cauti astazi?"]')
    SEARCH_BUTTON_XPATH = (By.XPATH, '//input[@class="submit-search"]')
    DROPDOWN_SELECTOR = (By.XPATH, '//select[@name="sortWidget"]')
    QUANTITY_SELECTOR = (By.XPATH, '//input[@class="txt2 quantity"]')
    CART_PAGE_HEADER_SELECTOR = (By.XPATH , '//h3[contains(text(),"Cos cumparaturi")]' )
    ELEM2_SLIDER = (By.XPATH, '//span[@id="sn-slider-max"]')
    LEGO_DUPLO_FILTER = (By.XPATH, '//input[@value="&#34LEGO Duplo&#34"]')
    LEGO_FRIENDS_FILTER = (By.XPATH, '//input[@value="&#34LEGO Friends&#34"]')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.evomag.ro/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()

    def tearDown(self):
        self.driver.quit()


    def test_add_to_your_cart(self):
        self.search_product_XPATH('lego')
        self.driver.find_element(*self.LEGO_DUPLO_FILTER).click()
        time.sleep(2)
        dropdown_sort = Select(self.driver.find_element(*self.DROPDOWN_SELECTOR))
        dropdown_sort.select_by_visible_text('Pret crescator')
        time.sleep(2)
        action = ActionChains(self.driver)
        elem2 = self.driver.find_element(*self.ELEM2_SLIDER)  # the right hand slider
        action.drag_and_drop_by_offset(elem2, -90, 0).perform()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//form[@class="add-to-cart addToCart-4137546"]//input[@value="ADAUGA IN COS"]').click()

    def test_cart_page_is_loading(self):
        self.search_product_XPATH('lego')
        self.driver.find_element(*self.LEGO_FRIENDS_FILTER).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//form[@class="add-to-cart addToCart-4075995"]//input[@value="ADAUGA IN COS"]').click()
        time.sleep(2)
        actual_page_header = self.driver.find_element(*self.CART_PAGE_HEADER_SELECTOR).text
        expected_page_header = 'Cos cumparaturi'
        self.assertEqual(actual_page_header,expected_page_header,'there is an error')


    def test_modify_your_cart(self):
        self.search_product_XPATH('lego')
        self.driver.find_element(*self.LEGO_FRIENDS_FILTER).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//form[@class="add-to-cart addToCart-4075995"]//input[@value="ADAUGA IN COS"]').click()
        time.sleep(2)
        self.driver.find_element(*self.QUANTITY_SELECTOR).clear()
        self.driver.find_element(*self.QUANTITY_SELECTOR).send_keys('2')
        self.driver.find_element(By.XPATH, '//a[@class="hidden changeQty"]').click()


    def search_product_XPATH(self, searched_item):
        self.driver.find_element(*self.SEARCH_INPUT_XPATH).send_keys(searched_item)
        self.driver.find_element(*self.SEARCH_BUTTON_XPATH).click()