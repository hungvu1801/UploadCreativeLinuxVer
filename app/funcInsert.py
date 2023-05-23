import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def decorator(func):
    def wrapper(*args, **kwargs):
        try:
            _ = func(*args, **kwargs)
            return 1
        except Exception as err:
            print(f'{err}')
            return 0
    return wrapper

def insertProductName(browser, productName):
    try:
        time.sleep(1)
        try:
            b_cancle = browser.find_element(By.XPATH, "//button[@id='onesignal-slidedown-cancel-button']")
            b_cancle.send_keys(Keys.ENTER)
        except Exception as err:
            print(f'{err}')
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='title'][@name='title']")))
        # Input product name
        i_productName = browser.find_element(By.XPATH, "//input[@id='title'][@name='title']")
        i_productName.send_keys(productName)
        time.sleep(1)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0

def insertCategoty(browser, categoryName):
    try:
        time.sleep(1)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@role='combobox']")))
        # Input category
        i_category = browser.find_element(By.XPATH, "//span[@role='combobox']")
        i_category.click()
        i_categoryInput = browser.find_element(By.XPATH, "//input[@type='search']")
        i_categoryInput.send_keys(categoryName)
        time.sleep(1)
        # do this
        # li_categoryInput = browser.find_elements(By.XPATH, "//li[@role='treeitem']")
        # Or
        i_categoryInput.send_keys(Keys.ENTER)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0

def insertPrice(browser, price):
    try:
        time.sleep(1)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='price'][@name='price']")))
        # Input Price
        i_price = browser.find_element(By.XPATH, "//input[@id='price'][@name='price']")
        i_price.send_keys(price)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0

def insertDescription(browser, description):
    try:
        time.sleep(2)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='description'][@id='description']")))
        # Input Description
        i_description = browser.find_element(
            By.XPATH, "//textarea[@name='description'][@id='description']"
            )
        i_description.send_keys(description)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0

def insertProductTag(browser, productTag):
    try:
        # Input Product Tags
        # i_productTag = browser.find_element(By.XPATH, "//input[@name='tags'][@id='tags']")
        i_productTag = browser.find_element(
            By.XPATH, "//div[@class='bootstrap-tagsinput']/input[@type='text']"
            )
        for tag in productTag:
            time.sleep(1)
            i_productTag.send_keys(tag + Keys.ENTER)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0

def insertProductImages(browser, listPic):
    try:
        for _ in range(0, 5):
            browser.find_element(By.TAG_NAME, "html").send_keys(Keys.DOWN)
        # This method needs to loop each time we upload one picture
        for pic in listPic:
            time.sleep(1)
            u_productImages = browser.find_element(
                By.XPATH, "//input[@type='file'][@name='product_images[]']"
                )
            u_productImages.send_keys(pic)
            time.sleep(1)
            try:
                # pop-ups windows
                alert = browser.switch_to.alert
                alert.accept()
            except Exception as err:
                print(f"{err}")
        return 1
    except Exception as err:
        print(f'{err}')
        return 0

def insertProductZip(browser, zipfile):
    try:
        time.sleep(1)
        # Upload Product Files (zip)
        u_productFileZip = browser.find_element(By.XPATH, "//input[@type='file'][@name='product_files']")
        u_productFileZip.send_keys(zipfile)
        time.sleep(1)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0
    
def checkBoxes(browser):
    try:
        for _ in range(0, 15):
            browser.find_element(By.TAG_NAME, "html").send_keys(Keys.DOWN)
        # Checkbox Discount detail
        i_discountDetail = browser.find_element(By.XPATH, "//input[@type='checkbox'][@name='in_discount_deals']")
        i_discountDetail.click()
        time.sleep(1)

        # Checkbox Pick n Mix
        i_pickNMix = browser.find_element(By.XPATH, "//input[@type='checkbox'][@name='in_byob']")
        i_pickNMix.click()
        time.sleep(1)

        # Checkbox Term and Conditions
        i_termNCond = browser.find_element(By.XPATH, "//ins[@class='iCheck-helper']")
        i_termNCond.click()
        time.sleep(1)
        return 1
    except Exception as err:
        print(f"{err}")
        return 0
    
def submit(browser):
    try:# click submit form
        time.sleep(10)
        b_submit = browser.find_element(By.XPATH, "//button[@type='submit'][@name='submitbutton']")
        b_submit.send_keys(Keys.ENTER)
        return 1
    except Exception as err:
        print(f"{err}")
        return 0

def newItem(browser):
    try:
        time.sleep(1)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Add a new graphic")))
        
        b_next = browser.find_element(By.LINK_TEXT, "Add a new graphic")
        b_next.click()
        return 1
    except Exception as err:
        print(f"{err}")
        return 0