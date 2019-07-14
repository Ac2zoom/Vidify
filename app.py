from flask import Flask
from flask import render_template
from google_images_download import google_images_download
from PIL import ImageFont, Image, ImageDraw
import cv2
import os
import GetSlides
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
