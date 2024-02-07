import unittest
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class TestFilterandOrder(unittest.TestCase):
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input.sn-suggest-input')
    SEARCH_INPUT_XPATH = (By.XPATH, '//input[@placeholder="ce cauti astazi?"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '.submit-search')
    SEARCH_BUTTON_XPATH = (By.XPATH, '//input[@class="submit-search"]')
    PRODUCT_LIST_CONTAINER = (By.CSS_SELECTOR, "div.product_grid")
    PRICES_SELECTOR = (By.CSS_SELECTOR, "span.real_price")
    DROPDOWN_SELECTOR = (By.CSS_SELECTOR, '#sortWidget')
    DROPDOWN_SELECTOR_XPATH = (By.XPATH, '//select[@name="sortWidget"]')
    ONDULATOARE_FILTER = (By.CSS_SELECTOR, '#c19jYXRlZ29yeSYjMzRPbmR1bGF0b2FyZSYjMzQ_')
    LEGO_DUPLO_FILTER = (By.XPATH, '//input[@value="&#34LEGO Duplo&#34"]')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.evomag.ro/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()

    def tearDown(self):
        self.driver.quit()


    def test_min_price(self):
        self.search_product_CSS('Smartwatch Huawei')
        product_list_container = self.driver.find_element(*self.PRODUCT_LIST_CONTAINER)  # the grid with all products found
        prices = product_list_container.find_elements(*self.PRICES_SELECTOR)  # the price of the products found
        price = []  # create an empty list

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',', '.').strip()  # [:-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
                if pret != 'N/A':
                    pret_convertit_float = float(pret)  # convert the prices in float
                    price.append(pret_convertit_float)  # add them to the price list
            except ValueError:
                print( f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

        print(f'prices are: {price}')  # print all prices
        lowest_price = min(price)
        print(f'the lowest price is : {lowest_price}')


    def test_filter(self):
        self.search_product_CSS('ondulator')
        self.driver.find_element(*self.ONDULATOARE_FILTER).click()
        time.sleep(2)
        action = ActionChains(self.driver)
        # elem1 = self.driver.find_element(By.CSS_SELECTOR, '#sn-slider-min')
        elem2 = self.driver.find_element(By.CSS_SELECTOR, '#sn-slider-max')
        action.drag_and_drop_by_offset(elem2, -140, 0).perform()  # in this way we can move the right side slider in left hand way
        time.sleep(2)
        product_list_container = self.driver.find_element(*self.PRODUCT_LIST_CONTAINER)
        prices = product_list_container.find_elements(*self.PRICES_SELECTOR)  # the price of the products found
        price = []  # create an empty list

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',','.').strip()  # [::-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
                if pret != 'N/A':
                    pret_convertit_float = float(pret)  # convert the prices in float
                    price.append(pret_convertit_float)  # add them to the price list
            except ValueError:
                print( f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

        print(f'prices are: {price}')  # print all prices

        interval = (29 , 351)
        for element in price:
            self.assertTrue(interval[0] <= element <= interval[1], f'error: the {element} element is not in the filter range' )


    def test_ascending_order(self):
        self.search_product_CSS('ondulator')
        dropdown_sort = Select(self.driver.find_element(*self.DROPDOWN_SELECTOR))
        dropdown_sort.select_by_value('f_price')
        time.sleep(3)
        prices = self.driver.find_elements(*self.PRICES_SELECTOR)  # the price of the products found
        price = []  # create an empty list

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',','.').strip()  # [:-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
                if pret != 'N/A':
                    pret_convertit_float = float(pret)  # convert the prices in float
                    price.append(pret_convertit_float)  # add them to the price list
            except ValueError:
                print(f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

        print(f'prices are: {price}')  # print all prices
        sorted_list = sorted(price)  # arrange the elements of the list in ascending order
        assert sorted_list == price, f'the products are not sorted properly'  # if the sorted list is equal to the original list, it means that the result list was indeed sorted in ascending order
        print('test ok')

    def test_descending_order(self):
        self.search_product_CSS('blender')
        time.sleep(2)
        dropdown_sortare = Select(self.driver.find_element(*self.DROPDOWN_SELECTOR))
        dropdown_sortare.select_by_value('-f_price')
        time.sleep(1)
        prices = self.driver.find_elements(*self.PRICES_SELECTOR)
        price = []

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',','.').strip()  # [:-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
                if pret != 'N/A':
                    pret_convertit_float = float(pret)  # convert the prices in float
                    price.append(pret_convertit_float)  # add them to the price list
            except ValueError:
                print(f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

        print(f'prices are: {price}')  # print all prices

        sorted_list = sorted(price)[::-1]  # aranjam lista price in ordine descrescatoare - sorted le aranjeaza crescator, dupa care [::-1] le inverseaza
        assert sorted_list == price, f'the products are not sorted properly'  # if the sorted list is equal to the original list, it means that the result list was indeed sorted in ascending order
        print('test ok')

    def test_filter_XPATH(self):
        self.search_product_XPATH('lego')
        self.driver.find_element(*self.LEGO_DUPLO_FILTER).click()
        time.sleep(1)
        dropdown_sort = Select(self.driver.find_element(*self.DROPDOWN_SELECTOR_XPATH))
        dropdown_sort.select_by_visible_text('Pret crescator')
        time.sleep(1)
        action = ActionChains(self.driver)
        elem2 = self.driver.find_element(By.XPATH, '//span[@id="sn-slider-max"]')  # the right hand slider
        action.drag_and_drop_by_offset(elem2, -90, 0).perform()
        time.sleep(3)
        product_list_container = self.driver.find_element(*self.PRODUCT_LIST_CONTAINER)
        prices = product_list_container.find_elements(*self.PRICES_SELECTOR)  # the price of the products found
        price = []  # create an empty list

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',','.').strip()  # [::-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
                if pret != 'N/A':
                    pret_convertit_float = float(pret)  # convert the prices in float
                    price.append(pret_convertit_float)  # add them to the price list
            except ValueError:
                print(
                    f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

        print(f'prices are: {price}')  # print all prices

        interval = (44, 149)
        for element in price:
            self.assertTrue(interval[0] <= element <= interval[1],f'error: the {element} element is not in the filter range')

    def search_product_CSS(self, searched_item):
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(searched_item)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def search_product_XPATH(self, searched_item):
        self.driver.find_element(*self.SEARCH_INPUT_XPATH).send_keys(searched_item)
        self.driver.find_element(*self.SEARCH_BUTTON_XPATH).click()
