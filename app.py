from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from google_images_download import google_images_download
from PIL import ImageFont, Image, ImageDraw
import cv2
import os
import GetSlides
import vidtext
from flask.json import jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    # Form for source and text
    return render_template('index.html')


# TODO: Endpoint to handle keywords
@app.route("/vidify", methods=['GET', 'POST'])
def vidify():
    source_url = request.args.get('source')
    text = request.args.get('text')
    # TODO: Summarize text (use Rock's functions)
    content = vidtext.summary(text)  # Return List
    # Call get_image and overlay_text_on_image iteratively
    for sentence in content:
        paths = get_image(sentence)
        # TODO: Use keyword as keyword, sentence as description
        overlay_text_on_image(sentence, sentence)
    # TODO: Modify HTML template to include multiple images
    return send_file("slides/" + content[0] + " no watermark.jpg")
