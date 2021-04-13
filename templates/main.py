#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri April 09 08:02:27 2021

@author: Aakash
"""

import requests
from bs4 import BeautifulSoup
import smtplib
import time
import pymongo
from pymongo import MongoClient


mongo = MongoClient("mongodb+srv://aakashv8900:aakashv8900@cluster0.2r0iu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mongo["myFirstDatabase"]
col = db["users"]



URL = 'https://www.amazon.com/Tracfone-Apple/B08CL4CCG2/ref=ss=iphone&qid=1617786209&sr=8-3'
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64)', 'Cache-Control': 'no-cache', "Pragma": "no-cache"}
desired_price = 195

def price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    avail = soup.find(id="availability").get_text()
    converted_price = price[1:-3]
    converted_price = int(float(converted_price))

    

    print(title.strip())
    print(converted_price)
    print(avail.strip())



price()

#while(True):
#    price()
#    time.sleep(60)