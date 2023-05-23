import os
from app.funcInsert import (insertProductName, insertCategoty, 
                        insertDescription, insertPrice, 
                        insertProductTag, insertProductImages, 
                        insertProductZip, checkBoxes, submit, newItem)
from app.funcReadFile import getPicsAndZip, getContent
import time

def uploadProductsSession(file, dataDir, browser):
    try:
        loopTimes = file.shape[0]
        browser = browser
        rowNum = 0
        while loopTimes > 0:
            try:
                idRow = str(file.iloc[rowNum, 0])
                prodDir = os.path.join(dataDir, idRow)
                listPic, zipfile = getPicsAndZip(prodDir)

                if not listPic or not zipfile:
                    loopTimes -= 1
                    rowNum += 1
                    break
                
                productName, description, price, categoryName, productTag = getContent(file, rowNum)

                if not insertProductName(browser, productName):
                    _ = input()
                if not insertCategoty(browser, categoryName):
                    _ = input()
                if not insertPrice(browser, price):
                    _ = input()
                if not insertDescription(browser, description):
                    _ = input()
                if not insertProductTag(browser, productTag):
                    _ = input() 
                if not insertProductImages(browser, listPic):
                    _ = input() 
                if not insertProductZip(browser, zipfile):
                    _ = input() 
                if not checkBoxes(browser):
                    _ = input()
                if not submit(browser):
                    _ = input()
                if not newItem(browser):
                    _ = input(newItem.__name__)
                loopTimes -= 1
                rowNum += 1
                time.sleep(20)
            except Exception as err:
                print(f'{err}')
                break
        return browser
    except Exception as err:
        print(f'{err}')
        return 0