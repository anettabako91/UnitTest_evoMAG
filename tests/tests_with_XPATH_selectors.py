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
driver.find_element(By.XPATH, '//button[contains(text(),"Accepta toate")]').click()

# test2 - verify if the accessed site is correct
def test_check_page():
    driver.find_element(By.XPATH, '//div[@class="lbhead"]') #searching the 'cattegory' button,
    # if it's ok, it means the site is ok

#test3-access the account button and click on login. Identify the user and password elements and insert incorrect values
#(incorrect values mean any values that are not recognized as a valid account)
def test_login():
    driver.find_element(By.XPATH, '//div[contains(text(),"Login")]').click()
    driver.find_element(By.XPATH, '//a[@class="BtnLoginHead"]').click()
    driver.find_element(By.XPATH,'//input[@name="LoginClientForm[Email]"]').send_keys('abds@gmail.com')
    driver.find_element(By.XPATH, '//input[@id="LoginClientForm_Password"]').send_keys('113456789')

#test4- Click on the "connect" button and verify that the correct error message is returned
def test_error_message():
    driver.find_element(By.XPATH, '//input[@value="INTRA IN CONT"]').click()
    error_message=driver.find_element(By.XPATH, '//div[@class="generic_error_message err1"]').text.strip()
    assert error_message=="Utilizatorul nu exista, va recomandam sa creati unul nou." , "the error message is not correct"
    print('the correct error message is returned')


#test5 - search a product and verify if at least 10 results were returned
def test_searching_products():
    driver.find_element(By.XPATH, '//input[@placeholder="ce cauti astazi?"]').send_keys('lego')
    time.sleep(2)
    driver.find_element(By.XPATH, '//input[@class="submit-search"]').click()
    time.sleep(2)
    product_list_container = driver.find_element(By.XPATH, '//div[@class="product_grid"]') #the grid with all products found
    products = product_list_container.find_elements(By.XPATH, '//div[@class="npi_name"]') #the name of the products found - a list of them
    print(f'we found {len(products)} products') #print the lenght of the products list
    assert len(products) >= 10 , f'the search resulted in less than 10 products ' #if the lenght is greater than 10, it means that the search resulted in more than 10 products
    print('test ok, we found more than 10 products')

#test6 - select the product with the lowest price
def test_min_price():
    product_list_container = driver.find_element(By.XPATH, '//div[@class="product_grid"]')
    prices = product_list_container.find_elements(By.XPATH, '//span[@class="real_price"]')  # the price of the products found
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

#test7 -  filter by category - any category you want - ex: lego duplo - sort the list of results in ascending order by price, then filter the price -> max value ~250 Lei
def test_filter_and_oder():
    driver.find_element(By.XPATH, '//input[@value="&#34LEGO Duplo&#34"]').click()
    time.sleep(2)
    dropdown_sort=Select(driver.find_element(By.XPATH, '//select[@name="sortWidget"]'))
    dropdown_sort.select_by_visible_text('Pret crescator')
    time.sleep(2)
    elem2 = driver.find_element(By.XPATH, '//span[@id="sn-slider-max"]') #the right hand slider
    ActionChains(driver).drag_and_drop_by_offset(elem2, -90, 0).perform()

#test8 - add a product in your cart, then modify the quantity
def test_add_to_your_cart():
    driver.find_element(By.XPATH, '//form[@class="add-to-cart addToCart-3845114"]//input[@value="ADAUGA IN COS"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//input[@class="txt2 quantity"]').clear()
    driver.find_element(By.XPATH, '//input[@class="txt2 quantity"]').send_keys('2')
    driver.find_element(By.XPATH, '//a[@class="hidden changeQty"]').click()


test_check_page()
time.sleep(3)
test_login()
time.sleep(3)
test_error_message()
time.sleep(3)

driver.find_element(By.XPATH, '//a[@id="main_logo"]').click() #back to the main site
time.sleep(3)

test_searching_products()
time.sleep(3)
test_min_price()
time.sleep(3)
test_filter_and_oder()
time.sleep(3)
test_add_to_your_cart()
time.sleep(3)



time.sleep(10)
