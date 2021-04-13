import requests
from bs4 import BeautifulSoup
import smtplib
import time
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

mongo = MongoClient("mongodb+srv://aakashv8900:aakashv8900@cluster0.2r0iu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mongo["myFirstDatabase"]
col = db["users"]

alldata = col.find({})
text = []
for data in alldata['name']:
    text = data
    
print(text)