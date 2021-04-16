#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 17:02:27 2021

@author: kaydee
"""
#import flask
from flask import Flask, redirect, url_for, request, render_template, send_file, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from Alignment import ChangePerspective
from vcopy import Model as vModel
import json
import numpy as np
import cv2
#local changes

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
PATH = ""



app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = "Content-Type"
cors = CORS(app)

@app.route("/")
def home():
    return render_template("main.html")


@app.route("/home",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/results") 
def res():
    global PATH
    if PATH == "":
        # TODO : add custom error mesage - Invalid PATH
        return render_template("index.html")
    vmod= vModel(PATH)
    sudoku = vmod.predictions
    sudoku_vals = sudoku.argmax(axis=1)
    sudoku_confidence_levels = sudoku.max(axis=1)
    sud_bools = sudoku_confidence_levels > 0.9
    sudoku_thresholded = sudoku_vals * sud_bools
    print(sudoku_confidence_levels)
    suddict = {'vals':"".join(map(str,sudoku_vals)), 'vals_with_conf':"".join(map(str,sudoku_thresholded))}
    print(suddict,PATH)
    with open("templates/sudoku.json","w") as f:
       json.dump(suddict,f)
       print("JSON written")
    return render_template("review.html",preds = [suddict])
    
    
    

@app.route("/output",methods=["GET","POST"])
def out():
    global PATH
    cpers = ChangePerspective()
    if request.method == "POST":
        img = request.files["img"]
        sfname = secure_filename(img.filename)
        img.save(app.config['UPLOAD_FOLDER']+sfname)
        fpath = os.path.join(app.config['UPLOAD_FOLDER'],sfname)
        
        print(sfname,app.config['UPLOAD_FOLDER'],fpath)
        cpers.readim(fpath,sfname)
        edited_sfname ="edited_"+sfname
        rel_image_path = "../static/images/"  
        PATH =os.path.join(app.config['UPLOAD_FOLDER'],edited_sfname)
        
        return render_template("result.html",inp = rel_image_path+sfname, out = rel_image_path+edited_sfname)
    return "no"
    
@app.route("/solve",methods=["GET","POST"])
def solve():
    if request.method == "POST":
        temp = ""
        for i in range(81):
            gres = request.form.get("c"+str(i))

            if gres == "":
                temp += "0"
            else:
                temp+=gres

        return render_template("solve.html",final_sudoku = [{"vals":temp}])
    return "fail"


@app.route("/api")
@cross_origin()
def api():
    return render_template("api.html")

@app.route("/api/get_json",methods=["GET","POST"])
@cross_origin()
def gjson():
    if request.method == "POST":
        file = request.files['img'].read()
        npimg = np.fromstring(file, np.uint8)
        img = cv2.imdecode(npimg,cv2.IMREAD_COLOR) 
        changePerspectiveImg = ChangePerspective()
        img = changePerspectiveImg.readim(img)

        vModel_api = vModel(img)
    else:
        return "No file found!"




    return jsonify(predictions = "".join(map(str,vModel_api.predictions.argmax(axis = 1))))

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
