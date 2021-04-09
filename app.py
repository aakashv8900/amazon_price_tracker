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
cors = CORS(app)
mongo = PyMongo(app)

@app.route('/',  methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template("main.html")

    

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if 'name' in request.files:
        name = request.files['name']
        mongo.save_file(name)
    if 'surl' in request.files:
        surl = request.files['surl']
        mongo.save_file(surl)
    if 'price' in request.files:
        price = request.files['price']
        mongo.save_file(price)
    if 'email' in request.files:
        email = request.files['email']
        mongo.save_file(email)
    mongo.db.users.insert({'email': request.form.get('email'), 'price': request.form.get('price'), 'surl': request.form.get('surl'), 'name': request.form.get('name')})
    return render_template("submit.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)