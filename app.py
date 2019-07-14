from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from google_images_download import google_images_download
from PIL import ImageFont, Image, ImageDraw
import os
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


# def make_slides(description_map):
"""
Loops through all the given keywords and generates slides by 
finding images for the keywords and overlaying their descriptions onto the images. 
Saves the resulting images in the 'slides' folder
@description_map:   a HashMap matching the keyword (String) with its description (String)
@return:            Saves resulting slides to 'slides' folder
"""


def get_image(keywords):
    """
    Finds all the images for the given keywords and downloads them into the downloads folder
    @keywords:  a comma separated list of keywords for images
    @return:    Saves the images to the downloads folder
    """
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keywords,
        "suffix_keywords": "no watermark",
        "format": "jpg",
        "aspect_ratio": "wide",
        "usage_rights": "labeled-for-reuse-with-modifications",
        "limit": 5,
        "size": "large",
        "print_urls": True}
    paths = response.download(arguments)
    return paths


def overlay_text_on_image(keyword, description):
    """
    Finds the image associated with that keyword and overlays the description over the top of it
    @keyword:       The title of the image that needs a description (String)
    @description:   Short sentence to overlay on the image (String)
    @return:        Saves the image to 'slides' folder
    """
    # for file in os.listdir("downloads\\" + keyword):
    #     if file.endswith(".jpg"):
    keyword = keyword + " no watermark"
    for file in os.listdir("downloads/" + keyword):
        filename = file
        
    img = Image.open("downloads/" + keyword + "/" + filename)

    draw = ImageDraw.Draw(img)

    # truetype(font.ttf, font-size)
    font = ImageFont.truetype("FancyHeartScript.ttf", 150)

    # text(position, text, color, font)
    draw.text((50, 50), description, (255, 100, 100), font=font)
    draw = ImageDraw.Draw(img)
    img.save("slides/" + keyword + ".jpg")

