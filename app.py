#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri April 09 08:02:27 2021

@author: Aakash
"""

import flask
from flask import Flask, url_for, request, render_template, jsonify
import os
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient


from flask import Flask
app = Flask(__name__)
app.testing = True
app.config['MONGO_URI'] = 'mongodb+srv://aakashv8900:aakashv8900@cluster0.2r0iu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app.config['MONGO_DBNAME'] = 'myFirstDatabase'
mongo = PyMongo(app)
db = mongo.db
col = mongo.db["users"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/form',  methods=['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template("main.html")

    
@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        surl = request.form.get('surl', type=str)
        price = request.form.get('price', type=int)
        email = request.form.get('email', type=str)   
        col.insert({'name':name, 'surl':surl, 'price':price, 'email':email})
        return render_template("submit.html", name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)