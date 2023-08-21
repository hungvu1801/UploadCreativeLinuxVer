
from app.funcLogIn import initBrowser, browseWebsite, logIn, goToAddGraphic
from app.funcReadFile import getDataDir, getFileExcel, readFileExcel
from app.funcUpload import uploadProductsSession
import os
import time

def readFilesSession():
    """ READ FILES SESSION"""
    fileName = getFileExcel()
    if not fileName:
        return 0

    file = readFileExcel(fileName)
    if file.empty:
        return 0
    
    dataDir = getDataDir(file)
    if not dataDir:
        return 0
    return file, dataDir
def logInSession():
    browser = initBrowser()
    if not browser:
        return 0
    browser = browseWebsite(browser)
    if not browser:
        return 0
    browser = logIn(browser)
    if not browser:
        return 0
    browser = goToAddGraphic(browser)
    if not browser:
        return 0
    return browser

def main():
    #########################################################################
    ######################### READ FILES SESSION ############################
    # file, dataDir = readFilesSession()
    # if file.empty or not dataDir:
    #     return 0

    #########################################################################
    ############################ LOG IN SESSION #############################

    browser = logInSession()
    if not browser:
        return 0
        
    #########################################################################
    ############################ UPLOAD SESSION #############################
    browser = uploadProductsSession(file, dataDir, browser)
    if not browser:
        return 0
    _ = input()
    browser.quit()
