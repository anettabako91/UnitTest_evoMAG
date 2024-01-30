import unittest
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


class TestAlerts(unittest.TestCase):

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

    def test_login(self):
        self.driver.find_element(By.XPATH, '//div[contains(text(),"Login")]').click()
        self.driver.find_element(By.XPATH, '//a[@class="BtnLoginHead"]').click()
        self.driver.find_element(By.XPATH, '//input[@name="LoginClientForm[Email]"]').send_keys('abds@gmail.com')
        self.driver.find_element(By.XPATH, '//input[@id="LoginClientForm_Password"]').send_keys('113456789')
        self.driver.find_element(By.XPATH, '//input[@value="INTRA IN CONT"]').click()
        error_message = self.driver.find_element(By.XPATH, '//div[@class="generic_error_message err1"]').text.strip()
        expected_message = "Utilizatorul nu exista, va recomandam sa creati unul nou."
        self.assertEqual(error_message,expected_message, "the error message is not correct")
        print('the correct error message is returned')

    def test_searching_products(self):
        self.search_product_CSS('Smartwatch Huawei')
        # self.driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('Smartwatch Huawei')  # search for huawei smartwatch
        # self.driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
        product_list_container = self.driver.find_element(By.CSS_SELECTOR, "div.product_grid")  # the grid with all products found
        products = product_list_container.find_elements(By.CSS_SELECTOR, ".npi_name")  # the name of the products found - a list of them
        print(f'we found {len(products)} products')  # print the lenght of the products list
        assert len(products) >= 10, f'the search resulted in less than 10 products '  # if the lenght is greater than 10, it means that the search resulted in more than 10 products
        print('test ok, we found more than 10 products')

    def test_min_price(self):
        self.search_product_CSS('Smartwatch Huawei')
        # self.driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('Smartwatch Huawei')  # search for huawei smartwatch
        # self.driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
        product_list_container = self.driver.find_element(By.CSS_SELECTOR, "div.product_grid")  # the grid with all products found
        prices = product_list_container.find_elements(By.CSS_SELECTOR,"span.real_price")  # the price of the products found
        price = []  # create an empty list

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',', '.').strip()  # [::-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
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
        # self.driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('ondulator')  # search for huawei smartwatch
        # self.driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
        self.driver.find_element(By.CSS_SELECTOR, '#c19jYXRlZ29yeSYjMzRPbmR1bGF0b2FyZSYjMzQ_').click()
        action = ActionChains(self.driver)
        elem1 = self.driver.find_element(By.CSS_SELECTOR, '#sn-slider-min')
        elem2 = self.driver.find_element(By.CSS_SELECTOR, '#sn-slider-max')
        action.drag_and_drop_by_offset(elem2, -140, 0).perform()  # in this way we can move the right side slider in left hand way
        # time.sleep(5)
        product_list_container = self.driver.find_element(By.CSS_SELECTOR, "div.product_grid")
        prices = product_list_container.find_elements(By.CSS_SELECTOR, "span.real_price")  # the price of the products found
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
        self.driver.implicitly_wait(5)

        interval = (29 , 315)
        for element in price:
            if not (interval[0] <= element <= interval[1]):
                print(f'error: the {element} element is not in the filter range')

    def test_ascending_order(self):
        self.search_product_CSS('ondulator')
        # self.driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('ondulator')  # search for ondulator
        # self.driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
        dropdown_sortare = Select(self.driver.find_element(By.CSS_SELECTOR, '#sortWidget'))
        dropdown_sortare.select_by_value('f_price')
        time.sleep(3)
        prices = self.driver.find_elements(By.CSS_SELECTOR, "span.real_price")  # the price of the products found
        price = []  # create an empty list

        for element in prices:
            try:
                pret = element.text[:-4].replace('.', '').replace(',','.').strip()  # [::-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
                if pret != 'N/A':
                    pret_convertit_float = float(pret)  # convert the prices in float
                    price.append(pret_convertit_float)  # add them to the price list
            except ValueError:
                print(f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

        print(f'prices are: {price}')  # print all prices
        sorted_list = sorted(price)  # arrange the elements of the list in ascending order
        assert sorted_list == price, f'the products are not sorted properly'  # if the sorted list is equal to the original list, it means that the result list was indeed sorted in ascending order
        print('test ok')

    def test_searching_products_XPATH(self):
        self.search_product_XPATH('lego')
        # self.driver.find_element(By.XPATH, '//input[@placeholder="ce cauti astazi?"]').send_keys('lego')
        # self.driver.find_element(By.XPATH, '//input[@class="submit-search"]').click()
        time.sleep(2)
        product_list_container = self.driver.find_element(By.XPATH, '//div[@class="product_grid"]')  # the grid with all products found
        products = product_list_container.find_elements(By.XPATH,'//div[@class="npi_name"]')  # the name of the products found - a list of them
        print(f'we found {len(products)} products')  # print the lenght of the products list
        assert len( products) >= 10, f'the search resulted in less than 10 products '  # if the lenght is greater than 10, it means that the search resulted in more than 10 products
        print('test ok, we found more than 10 products')

    def test_filter_XPATH(self):
        self.search_product_XPATH('lego')
        # self.driver.find_element(By.XPATH, '//input[@placeholder="ce cauti astazi?"]').send_keys('lego')
        # self.driver.find_element(By.XPATH, '//input[@class="submit-search"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//input[@value="&#34LEGO Duplo&#34"]').click()
        dropdown_sort = Select(self.driver.find_element(By.XPATH, '//select[@name="sortWidget"]'))
        dropdown_sort.select_by_visible_text('Pret crescator')
        time.sleep(2)
        action = ActionChains(self.driver)
        elem2 = self.driver.find_element(By.XPATH, '//span[@id="sn-slider-max"]')  # the right hand slider
        action.drag_and_drop_by_offset(elem2, -90, 0).perform()

    def test_add_to_your_cart(self): #this works only if the product with '//form[@class="add-to-cart addToCart-4137546"]//input[@value="ADAUGA IN COS"]' XPATH is still available
        self.search_product_XPATH('lego')
        # self.driver.find_element(By.XPATH, '//input[@placeholder="ce cauti astazi?"]').send_keys('lego')
        # self.driver.find_element(By.XPATH, '//input[@class="submit-search"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//input[@value="&#34LEGO Duplo&#34"]').click()
        time.sleep(2)
        dropdown_sort = Select(self.driver.find_element(By.XPATH, '//select[@name="sortWidget"]'))
        dropdown_sort.select_by_visible_text('Pret crescator')
        time.sleep(2)
        action = ActionChains(self.driver)
        elem2 = self.driver.find_element(By.XPATH, '//span[@id="sn-slider-max"]')  # the right hand slider
        action.drag_and_drop_by_offset(elem2, -90, 0).perform()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//form[@class="add-to-cart addToCart-4137546"]//input[@value="ADAUGA IN COS"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//input[@class="txt2 quantity"]').clear()
        self.driver.find_element(By.XPATH, '//input[@class="txt2 quantity"]').send_keys('2')
        self.driver.find_element(By.XPATH, '//a[@class="hidden changeQty"]').click()


    def search_product_CSS(self, searched_item):
        self.driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys(searched_item)
        self.driver.find_element(By.CSS_SELECTOR, '.submit-search').click()


    def search_product_XPATH(self,searched_item):
        self.driver.find_element(By.XPATH, '//input[@placeholder="ce cauti astazi?"]').send_keys(searched_item)
        self.driver.find_element(By.XPATH, '//input[@class="submit-search"]').click()