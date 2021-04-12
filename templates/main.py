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


URL = 'https://www.amazon.com/Tracfone-Apple-iPhone-Prepaid-Smartphone/dp/B08CL4CCG2/ref=sr_1_3?dchild=1&keywords=iphone&qid=1617786209&sr=8-3'
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

    if(converted_price > desired_price):
        send_mail()

    print(title.strip())
    print(converted_price)
    print(avail.strip())

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('aakashv.8292@gmail.com', 'uqyqrkresxpodqhs')
    subject = 'PRICE FELL DOWN!'
    body = 'Check the amazon link - https://www.amazon.com/Tracfone-Apple-iPhone-Prepaid-Smartphone/dp/B08CL4CCG2/ref=sr_1_3?dchild=1&keywords=iphone&qid=1617786209&sr=8-3'

    msg = f"Subject: {subject}\n\n{body}"

    reciever = 'aakashv.1238900@gmail.com'

    server.sendmail(
        'aakashv.8292@gmail.com',
        reciever,
        msg
    )
    print('HEY MAIL HAS BEEN SENT!')

    server.quit()

price()

#while(True):
#    price()
#    time.sleep(60)