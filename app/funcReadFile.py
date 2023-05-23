import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def getFileExcel():
    ''' Return the info files'''
    try:
        # logging.debug('Start of fetch_files')
        root = tk.Tk()
        root.withdraw()
        # Open file reader
        fileName = filedialog.askopenfilename(title='Import files')
        if not fileName:
            return 0
        return fileName

    except Exception as err:
        print(f'{err}')
        return 0
    
def readFileExcel(fileName):
    try:
        file = pd.read_excel(fileName)
        return file
    except Exception as err:
        print(f'{err}')
        return pd.DataFrame()
    
def getDataDir(file):
    root = tk.Tk()
    root.withdraw()
    # Open file reader
    dataDir = filedialog.askdirectory()
    if not dataDir:
        return 0
    checkValidity = checkDataDir(file, dataDir)
    while not checkValidity:
        print('Data directory invalid. Please try again.')
        dataDir = filedialog.askdirectory()
        if not dataDir:
            return 0
        checkValidity = checkDataDir(file, dataDir)
    return dataDir

def getPicsAndZip(dataDir):
    try:
        listPic = list()
        for f in os.listdir(dataDir):
            _, extension = os.path.splitext(f)
            if extension == ".jpg" or extension == ".png":
                fileName = os.path.join(dataDir, f)
                listPic.append(fileName)
            else:
                zipfile = os.path.join(dataDir, f)
        return listPic, zipfile
    except Exception as err:
        print(f'{err}')
        return list(), 0

def checkDataDir(file, dataDir):
    try:
        idRow = str(file.iloc[0, 0])
        testDir = os.path.join(dataDir, idRow)
        _ = os.listdir(testDir)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0
    
def getContent(file, rowNum):
    productName = file.iloc[rowNum, 1]
    description = file.iloc[rowNum, 2]
    price = file.iloc[rowNum, 3]
    categoryName = file.iloc[rowNum, 4]
    productTag = file.iloc[rowNum, 5].split(",")
    return productName, description, price, categoryName, productTag