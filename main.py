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

alldata = col.find({})
for data in alldata:
    name = data['name']
    URL = data['surl']
    desired_price = data['price']
    reciever = data['email']

    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64)', 'Cache-Control': 'no-cache', "Pragma": "no-cache"}

    def price():
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            title = soup.find(id="productTitle").get_text()
            price = soup.find(id="priceblock_ourprice").get_text()
            avail = soup.find(id="availability").get_text()
            converted_price = price[1:-3]
            converted_price = int(float(converted_price))
                
            if(converted_price > desired_price):
                send_mail()
                col.delete_one(reciever) 
        except:
            pass

    def send_mail():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('aakashv.8292@gmail.com', 'uqyqrkresxpodqhs')
        subject = 'PRICE FELL DOWN!'
        body = 'Check the amazon link - ' + URL

        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail(
            'aakashv.8292@gmail.com',
            reciever,
            msg
        )
        server.quit()
while(True):
    price()
    time.sleep(60)