import time


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.maximize_window()

# - Test 1: access the evomag site https://www.evomag.ro/
driver.get("https://www.evomag.ro/")

time.sleep(3)

# accept gdpr
driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()

# test2 - verify if the accessed site is correct
def test_check_page():
    driver.find_element(By.CSS_SELECTOR, '.lbhead') #searching the 'cattegory' button, if it's ok, it means the site is ok

#test3 - get the title of the page and verify if it is correct
def test_title():
    title = driver.title
    assert title=='evoMAG.ro - Electronice si electrocasnice la un pret bun' ,f'there is an error in the title'
    print(f'the title is <{title}> and it is correct')


#test4 - search a product and verify if at least 10 results were returned
def test_searching_products():
    driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('Smartwatch Huawei') #search for huawei smartwatch
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
    time.sleep(2)
    product_list_container = driver.find_element(By.CSS_SELECTOR, "div.product_grid") #the grid with all products found
    products = product_list_container.find_elements(By.CSS_SELECTOR, ".npi_name") #the name of the products found - a list of them
    print(f'we found {len(products)} products') #print the lenght of the products list
    assert len(products) >= 10 , f'the search resulted in less than 10 products ' #if the lenght is greater than 10, it means that the search resulted in more than 10 products
    print('test ok, we found more than 10 products')

#test5 - select the product with the lowest price

def test_min_price():
    # driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('Smartwatch Huawei')  # search for huawei smartwatch
    # time.sleep(2)
    # driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
    # time.sleep(2)
    product_list_container = driver.find_element(By.CSS_SELECTOR, "div.product_grid")  # the grid with all products found
    prices = product_list_container.find_elements(By.CSS_SELECTOR, "span.real_price")  # the price of the products found
    price = [] #create an empty list

    for element in prices:
        try:
            pret = element.text[:-4].replace('.','').replace(',', '.').strip() #[::-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
            if pret != 'N/A':
                pret_convertit_float = float(pret) #convert the prices in float
                price.append(pret_convertit_float) #add them to the price list
        except ValueError:
            print(f'error at the conversion of value: {element.text}') #print this message if there is an error in converting a value

    print(f'prices are: {price}') #print all prices
    lowest_price = min(price)
    print(f'the lowest price is : {lowest_price}')

#test6 - search for a product, filter by category - any category you want, and then filter by price, then check that all returned
# products have a price within the filter range
def test_filter():
    driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').clear()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('ondulator')  # search for ondulator
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#c19jYXRlZ29yeSYjMzRPbmR1bGF0b2FyZSYjMzQ_').click()
    time.sleep(2)
    elem1=driver.find_element(By.CSS_SELECTOR, '#sn-slider-min')
    elem2=driver.find_element(By.CSS_SELECTOR, '#sn-slider-max')
    #ActionChains(driver).drag_and_drop_by_offset(elem1, 17, 0).perform() #in this way we can move the left side slider in right hand way
    ActionChains(driver).drag_and_drop_by_offset(elem2, -140, 0).perform() #in this way we can move the right side slider in left hand way
    #two other options:
    #ActionChains(driver).click_and_hold(elem2).pause(1).move_by_offset(0, 17).release().perform()
    #ActionChains(driver).move_to_element(elem1).pause(1).click_and_hold(elem1).move_by_offset(17, 0).release().perform()
    time.sleep(2)
    product_list_container = driver.find_element(By.CSS_SELECTOR, "div.product_grid")
    prices = product_list_container.find_elements(By.CSS_SELECTOR, "span.real_price")  # the price of the products found
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
    time.sleep(3)

    for element in price:
        if 29 <= element <= 315:
            print(f'{element} face parte din intervalul filtrat')
        else:
            print(f'{element} nu face parte din intervalul filtrat')


# - Test7: search for a products, sort the list of results in ascending order by price and check that the products were really sorted
def test_ascending_order():
    driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').clear()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'input.sn-suggest-input').send_keys('ondulator')  # search for ondulator
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.submit-search').click()
    time.sleep(2)
    dropdown_sortare = Select(driver.find_element(By.CSS_SELECTOR, '#sortWidget'))
    dropdown_sortare.select_by_value('f_price')
    time.sleep(1)
    prices = driver.find_elements(By.CSS_SELECTOR, "span.real_price")  # the price of the products found
    price = []  # create an empty list

    for element in prices:
        try:
            pret = element.text[:-4].replace('.', '').replace(',', '.').strip()  # [::-4] -> to cut 'Lei' , first replace to cut the ., second replace to change the ',' to '.'
            if pret != 'N/A':
                pret_convertit_float = float(pret)  # convert the prices in float
                price.append(pret_convertit_float)  # add them to the price list
        except ValueError:
            print(f'error at the conversion of value: {element.text}')  # print this message if there is an error in converting a value

    print(f'prices are: {price}')  # print all prices
    sorted_list = sorted(price)  # arrange the elements of the list in ascending order
    assert sorted_list == price, f'the products are not sorted properly'  # if the sorted list is equal to the original list, it means that the result list was indeed sorted in ascending order
    print('test ok')


#run test2
test_check_page()

#run test5
test_title()

#run test4
test_searching_products()

#run test5
#test_min_price()

#run test6
test_filter()

#run test7
#test_ascending_order()

time.sleep(10)