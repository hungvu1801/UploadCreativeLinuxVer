# Chrome driver
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def initBrowser():
    try:
        # Config options
        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled") 
            # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        
        # Turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False) 
        ###########################################################################

        options.page_load_strategy = 'normal'

        options.add_argument('--disable-dev-shm-usage')

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # useragentSpoofing = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

        # browser.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentSpoofing}) 

        # print(browser.execute_script("return navigator.userAgent;"))

        # Changing the property of the navigator value for webdriver to undefined 
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

        return browser
    except Exception as err:
        print(f'{err}')
        input()
        return 0

def browseWebsite(browser):
    try:
        browser.get('https://www.google.com/')
        # browser.get('https://www.creativefabrica.com/')
        _ = input()
        browser.implicitly_wait(10)
        time.sleep(2)
        return browser
    except Exception as err:
        print(f'{err}')
        input()
        browser.quit()
        return 0

def logIn(browser):
    try:
        time.sleep(2)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='email']")))
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password']")))
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit']")))
        i_email = browser.find_element(By.XPATH, "//input[@type='email']")
        i_email.send_keys("equihuadino935632@gmail.com")

        i_pass = browser.find_element(By.XPATH, "//input[@type='password']")
        i_pass.send_keys("9ABXvC%T5s4aE")

        b_submit = browser.find_element(By.XPATH, "//button[@type='submit']")
        b_submit.send_keys(Keys.ENTER)
        
        return browser
    except Exception as err:
        print(f'{err}')
        input()
        browser.quit()
        return 0
    
def goToAddGraphic(browser):
    try:
        time.sleep(2)
        _ = input("Press enter if ready.")
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Add Graphic")))
        l_addGrapic = browser.find_element(By.LINK_TEXT, "Add Graphic")
        l_addGrapic.click()
        time.sleep(4)
        # press the cancel pop buttons
        try:
            b_cancle = browser.find_element(By.XPATH, "//button[@id='onesignal-slidedown-cancel-button']")
            b_cancle.send_keys(Keys.ENTER)
        except Exception as err:
            print(f'{err}')
        return browser
    except Exception as err:
        print(f'{err}')
        input()
        browser.quit()
        return 0