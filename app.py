from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename='scrapper.log',level=logging.INFO)

app=Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)