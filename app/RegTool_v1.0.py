
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import sys
import pandas as pd
import time
import random
import re
import warnings
import requests
from lxml.html import fromstring
import unittest

'''
Version 1.1.2 update log: 
- Clean code.
- Handle exception at get_best_buy(): if url is invalid return None.
- Modify function get_best_buy(): add information 'Other People want this.'
- Modify table: add column 'other_want_this'.
- Save pivot table to file.csv first, then add other columns: 'best_seller', 'other_want_this'.
'''

def changeDirectory():
    '''
    Change current saving directory to ./Dowloads/Etsy_ratings.
    '''
    os.chdir('C:'+os.environ.get('HOMEPATH') + '\\Downloads')
    try: 
        os.mkdir('Etsy_ratings')
    except Exception:
        pass
    os.chdir('C:'+os.environ.get('HOMEPATH') + '\\Downloads\\Etsy_ratings')
    print('Please get your .csv file at directory: %s.' % os.getcwd())

def get_item():
    '''
    Find items' ratings, items' name and items' url which then pulled into a data frame.
    '''
    # Find item rating
    try:
        ratings = browser.find_elements_by_xpath('//div[@class="mb-xs-0 p-xs-0"]/span/input[1]')
    except:
        print('Error in xpath review.')
        
    # Find item names and urls
    try:
        reviews = browser.find_elements_by_xpath('//div[@class="mt-xs-3 clearfix"]')
    except:
        print('Error in xpath review.')
    # Find items urls
    link_list = []
    for i in range(0, len(reviews)):    
        try:
            link_list.append(reviews[i].find_element_by_tag_name('a').get_property('href'))
        except Exception:
            link_list.append('This listing is no longer available')
    
    rating_list = [ratings[i].get_property('value') for i in range(0, len(ratings))]
    name_list = [reviews[i].text for i in range (0, len(reviews))]
    df = pd.DataFrame({'Name': name_list, 'url': link_list, 'Rating': rating_list})
    return df

def get_best_buy(x):
    '''
    Return if a product has a bestseller brand or not.
        Param: 
            x (string): an url of certain product.
        Return:
            bs (string): Bestseller.
            opwt (string): Other people want this.
    '''
    headers = {
    'authority': 'www.etsy.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document'
    }

    time.sleep(random.randint(1, 5))
    bs = ''
    opwt = ''
    try:
        source = requests.get(x, headers=headers).text
    except Exception:
        # If url is invalid then return to None
        return bs, opwt
    soup = fromstring(source)
    # Find if 'Bestseller' exists
    if soup.xpath('//span[@class="wt-badge wt-badge--status-03  wt-mt-xs-1 wt-mr-xs-1 "]\
                    /div/span[contains(text(),"Bestseller")]'):
        bs = 'Bestseller'
    # Find if 'other people have this in their basket' exists 
    if soup.xpath('.//p[@class="wt-position-relative wt-text-caption"]/text()[2]'):
        opwt = soup.xpath('.//p[@class="wt-position-relative wt-text-caption"]/text()[2]')[0].strip()
    return bs, opwt

def scraping_da_net():
    '###############################  Declare variables  ###############################'
    # Pass as long as valid url
    while True:
        MAIN_PAGE = input("Please enter shop's url: ")
        if re.findall('(https://www.etsy.com/shop/)([a-zA-Z0-9]*)', MAIN_PAGE):
            break
        else:
            print(' WARNING!!! '.center(50, '#'))
            print('This is not a valid url. Please try again.')
            continue
    # Pass as long as valid number
    while True:  
        try:  
            PAGES = int(input('Please enter number of pages: '))
        except Exception as err:
            print(' WARNING!!! '.center(50, '#'))
            print('Please enter a valid number. Error: ', err)
            continue
        else:
            break
    
    exitloop = False
    page = 1
    df_all = pd.DataFrame(columns=['Name', 'url', 'Rating'])
    
    '##############################  Initiate web brower  ##############################'
    time.sleep(2)
    browser.get(MAIN_PAGE)
    
    '##################################  Scrape main  ##################################'
    print('Scraping %s' % MAIN_PAGE)
    print('Scraping Page no %i' % page)
    print('Waiting...')
    while page < PAGES and exitloop == False:
        time.sleep(random.randint(5, 10))
        html_elem = browser.find_element_by_tag_name('html')
        html_elem.send_keys(Keys.END)
        df_all = pd.concat([df_all, get_item()], sort=False, ignore_index=True)
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, 'Next page'))
            )
            if len(browser.find_elements_by_partial_link_text('Next page')) == 1:
                browser.find_elements_by_partial_link_text('Next page')[0].click()
            else:
                browser.find_elements_by_partial_link_text('Next page')[-1].click()
            time.sleep(4)
            page += 1
            print('Scraping Page no %i' % page)
            print('Waiting...')
        except Exception as err:
            print(err)
            exitloop = True
            print('Final page: ', page)
    
    '##################################  Return data  ##################################'
    df_all['Rating'] = df_all['Rating'].astype('int')

    try:
        table = df_all.pivot_table(index=['Name', 'url'], values=['Rating'], aggfunc='count').reset_index()
    except Exception as err:
        print(' WARNING!!! '.center(50, '#'))
        table = df_all
    
    if re.findall('(https://www.etsy.com/shop/)([a-zA-Z0-9]*)', MAIN_PAGE):
        name_file = re.findall('(https://www.etsy.com/shop/)([a-zA-Z0-9]*)', MAIN_PAGE)[0][1]
    else:
        name_file = 'no_name'
    # Save table first
    table.to_csv(name_file + '.csv')
    
    best_seller_lst = []
    opwt_lst = []
    for url in table['url']:
        best_seller, opwt = get_best_buy(url)
        best_seller_lst.append(best_seller)
        opwt_lst.append(opwt)
    # Create a temporary dataframe contained 'best_seller' and 'other_want_this'
    temp_df = pd.DataFrame({'best_seller': best_seller_lst, 'other_want_this': opwt_lst}, 
                           columns=['best_seller', 'other_want_this'])
    # Merge table with temp_df
    table = table.merge(temp_df, on=table.index)
    try:
        table.drop(['key_0'], axis=1, inplace=True)
    except Exception:
        pass
    table.to_csv(name_file + '.csv')
    print('Scraping completed.')

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('= '*60)
    print('SCRAPING TOOL ETSY.COM'.center(120))
    print('COPYRIGHT © THUY TEAM'.center(120))
    print('version 1.10'.center(120))
    print('\n')
    print('Email hỗ trợ: vutienhung2212@gmail.com'.center(120))
    print('= '*60)   

    ans = 'y'
    if getattr(sys, 'frozen', False): 
        # executed as a bundled exe, the driver is in the extracted folder
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        browser = webdriver.Chrome(chromedriver_path)
    else:
        # executed as a simple script, the driver should be in `PATH` bc
        browser = webdriver.Chrome()
        browser2 = webdriver.Chrome()

    time.sleep(2)
    changeDirectory()
    
    while ans.lower() == 'y':
        scraping_da_net()
        ans = input('Do you want to scrape another Shop: Press [Y]: Yes   [N]: No ')

    browser.quit()
    browser2.quit()