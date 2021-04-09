#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri April 09 08:02:27 2021

@author: Aakash
"""

import flask
from flask import Flask, redirect, url_for, request, render_template, send_file, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import json
import numpy as np
from flask_wtf import Form, FlaskForm
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient


from flask import Flask
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://aakashv8900:aakashv8900@cluster0.2r0iu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app.config['MONGO_DBNAME'] = 'myFirstDatabase'
mongo = PyMongo(app)
db = mongo.db
col = mongo.db["users"]

@app.route('/',  methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template("main.html")

    

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if 'name' in request.files:
            name = request.files['name']
            col.save_file(name)
        if 'surl' in request.files:
            surl = request.files['surl']
            col.save_file(surl)
        if 'price' in request.files:
            price = request.files['price']
            col.save_file(price)
        if 'email' in request.files:
            email = request.files.get['email']
            col.save_file(email)
        col.insert_one({'name': request.form.get('name'), 'surl': request.form.get('surl'), 'price': request.form.get('price'), 'email': request.form.get('email')})
    return render_template("submit.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)