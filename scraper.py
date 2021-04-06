import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

URL = 'https://www.amazon.in/New-Apple-iPhone-12-128GB/dp/B08L5TNJHG/ref=sr_1_4?dchild=1&keywords=iphone&qid=1617730979&sr=8-4'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
}
driver = webdriver.Firefox(executable_path=r'your\path\geckodriver.exe')


driver.get(URL)

time.sleep(5)

page = driver.page_source

driver.close()

soup = BeautifulSoup(page, 'html5lib')
title = soup.find(id="productTitle").text()
price = soup.find(id="priceblock_ourprice").text()
converted_price = float(price[0:9])

if(converted_price < 85,000):
    send_mail()

print(title.strip())
print(converted_price)