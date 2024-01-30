# Selectors - project Evomag 

## Introduction

After learning about selenium and selectors at the course, I wanted to create a project based on what I learned,to deepen the information received and to practice as much as possible.
In this project I chose to work on the evoMAG website, an online store for electronics, household appliances and many others.
I created an automation testing project using PyCharm, emphasizing Selenium WebDriver, CSS selectors, and XPATH selectors. This project focuses on testing the functionalities of a webshop, 
an integral component of the e-commerce ecosystem. My objective is to create an efficient automation testing suite that can simulate user interactions, and navigate through the webshop's 
various pages. This includes product searches, adding items to the shopping cart, and navigating through the login process.

## Technical information

1. **PyCharm:** Serving as our primary IDE, PyCharm provides a comprehensive environment for Python development, offering features that enhance coding productivity.

2. **Selenium WebDriver:** Selenium is a powerful automation tool that enables us to control and interact with web browsers programmatically. By utilizing Selenium WebDriver, we can automate
   the testing process by emulating user actions such as clicks, form submissions, and data input. To use the selenium library, we must import it using the insert instruction, from which we must
   import the webdriver class

3. **CSS Selectors:** A CSS selector is a string of characters used to identify elements in the HTML code in order to be able to interact with them and check their functionality.
   It is generally considered that a CSS selector is faster than XPATH, but its disadvantage is that it can only search from top to bottom (from parent to child) and not vice versa, as with XPATH.

4. **XPATH Selectors:** XPath is another powerful selector strategy that aids in navigating through the HTML structure of a web page. Utilizing XPATH selectors enhances our ability to locate elements
   based on their hierarchical position in the document object model.

5. **Additional Selenium Modules:**
   ```python
   from selenium import webdriver
   from selenium.webdriver import ActionChains
   from selenium.webdriver.common.by import By
   from selenium.webdriver.support.select import Select
   ```
   -where ActionChains class is used to interact with the price filtering slider:
   ```python
   elem2 = driver.find_element(By.XPATH, '//span[@id="sn-slider-max"]') #the right hand slider
   ActionChains(driver).drag_and_drop_by_offset(elem2, -90, 0).perform()
   ```
   -and the Select class for interacting with dropdown menus:
   ```python
   dropdown_sort=Select(driver.find_element(By.XPATH, '//select[@name="sortWidget"]'))
   dropdown_sort.select_by_visible_text('Pret crescator')
   ```

## Tests made with CSS selectors

The first step in starting any automation testing project is instantiating the driver, that is, creating an object from the class of the browser we are working with. In the example below, I have created 
an object from the Chrome class, through which we will have access to all the attributes and methods through which we will be able to interact with the browser.
```python
driver = webdriver.Chrome()
driver.maximize_window()
```

The next, very important step is to access the evoMAG webshop, and the acceptance of cookies. This initial step serves as the foundation for subsequent interactions.
```python
driver.get("https://www.evomag.ro/")
driver.find_element(By.CSS_SELECTOR, '.gdpr-btn').click()
```

After that, several tests follow, including:
  - verifying the correctness of the accessed site,
  - seeking assurance in page title,
  - searching and selecting different products,
  - filtering by category and price,
  - sorting the list of results in ascending order, etc
  
## Tests made with XPATH selectors

As above, first of all,I have created an object from the Chrome class, accessed the evoMAG webshop, and accepted the cookies.
The tests were similar to the ones above, the difference being the use of XPATH selectors for element identification.
\
At the same time, I also created a login-based test, where I identified the user and password elements, entered incorrect data and tried to connect. 
The purpose of this test was to check if the error message returned was the correct one.
```python
def test_login():
    driver.find_element(By.XPATH, '//div[contains(text(),"Login")]').click()
    driver.find_element(By.XPATH, '//a[@class="BtnLoginHead"]').click()
    driver.find_element(By.XPATH,'//input[@name="LoginClientForm[Email]"]').send_keys('abds@gmail.com')
    driver.find_element(By.XPATH, '//input[@id="LoginClientForm_Password"]').send_keys('113456789')
test_login()
```
\
Last but not least, I tested the functionality of adding products to the shopping cart, deleting and updating it - it should be mentioned that this test 
is only valid until the respective product is in stock.
```python
def test_add_to_your_cart():
    driver.find_element(By.XPATH, '//form[@class="add-to-cart addToCart-3845114"]//input[@value="ADAUGA IN COS"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//input[@class="txt2 quantity"]').clear()
    driver.find_element(By.XPATH, '//input[@class="txt2 quantity"]').send_keys('2')
    driver.find_element(By.XPATH, '//a[@class="hidden changeQty"]').click()
test_add_to_your_cart()
```
\
The entire project can be found here: [CSS_Selectors](https://github.com/anettabako91/Selectors_Test-Evomag/blob/main/tests/tests_with_CSS_selectors.py) 
and [XPATH_Selectors](https://github.com/anettabako91/Selectors_Test-Evomag/blob/main/tests/tests_with_XPATH_selectors.py)

