# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 19:53:37 2021

@author: karunpabbi
"""

from io import BytesIO
from zipfile import ZipFile
import urllib.request
from datetime import date,timedelta
import pandas as pd
import schedule
import time
import datetime
import requests

def setDataToSite():
    url = "http://34.122.251.120/upload/"    
    files = {'file' : open("loader.csv","rb")}
    r = requests.post(url,files=files)
    print("ADDING DATA STATUS CODE : ",r.status_code)
    #print(r.content)  


def getDataBSE():

    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    
    opener = AppURLopener()
    
    weekdayNum=datetime.datetime.now().weekday()
    print(weekdayNum)
    
    crntTime=time.strftime("%H:%M")
    
    if weekdayNum<5:
        if crntTime < '18:00':
            print(weekdayNum)
            if(weekdayNum==0):
                dateUsed = (date.today() - timedelta(days = 3)).strftime("%d%m%y")
                print(dateUsed)
            else:
                dateUsed = (date.today() - timedelta(days = 1)).strftime("%d%m%y")
                print(dateUsed)
                
            
            print("BEFORE 6 PM ")
            
            
            print(dateUsed)
            url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+dateUsed+'_CSV.ZIP'
           # url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ250221_CSV.ZIP'
            print(url)
            response = opener.open(url)
            
            zipfile = ZipFile(BytesIO(response.read()))
            print(zipfile.namelist())
            
            dateFile='EQ'+dateUsed+'.CSV'
            
            df = pd.read_csv(zipfile.open(dateFile))

            df.to_csv('loader.csv',index=False)
            
            setDataToSite()
            

            
        else:
            
            print("AFTER 6 PM ")
            
            dateUsed = date.today().strftime("%d%m%y")
            print(dateUsed)
            url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+dateUsed+'_CSV.ZIP'
           # url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ250221_CSV.ZIP'
            print(url)
            response = opener.open(url)
            
            zipfile = ZipFile(BytesIO(response.read()))
            print(zipfile.namelist())
            
            dateFile='EQ'+dateUsed+'.CSV'
            
            df = pd.read_csv(zipfile.open(dateFile))

            df.to_csv('loader.csv',index=False)
            
            setDataToSite()
            

            
    else:
        
          print("WEEKENDS")
        
          dateUsed = (date.today() - timedelta(days = weekdayNum-4)).strftime("%d%m%y")
          print(dateUsed)
          url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+dateUsed+'_CSV.ZIP'
        
          print(url)
          response = opener.open(url)
         
          zipfile = ZipFile(BytesIO(response.read()))
          print(zipfile.namelist())
         
          dateFile='EQ'+dateUsed+'.CSV'
         
          df = pd.read_csv(zipfile.open(dateFile))

          df.to_csv('loader.csv',index=False)
          
          setDataToSite()
         

    
getDataBSE()

schedule.every().day.at("18:00").do(getDataBSE)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
    