from flask import Flask
from flask import render_template
from google_images_download import google_images_download
from PIL import ImageFont
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

# """
# Loops through all the given keywords and generates slides by 
# finding images for the keywords and overlaying their descriptions onto the images. 
# Saves the resulting images in the 'slides' folder
# @description_map:   a HashMap matching the keyword (String) with its description (String)
# @return:            Saves resulting slides to 'slides' folder
# """
# def make_slides(description_map):


"""
Finds all the images for the given keywords and downloads them into the downloads folder
@keywords:  a comma separated list of keywords for images
@return:    Saves the images to the downloads folder
"""
def get_image(keywords):
    
    arguments = {"keywords":keywords,
    "suffix_keywords":"no watermark",
    "format":"jpg",
    "aspect_ratio":"wide",
    "usage_rights":"labeled-for-reuse-with-modifications",
    "limit":5,
    "size":"large",
    "print_urls":True}
    paths = response.download(arguments)
    # images are now downloaded into the downloads folder

# """
# Finds the image associated with that keyword and overlays the description over the top of it
# @keyword:       The title of the image that needs a description (String)
# @description:   Short sentence to overlay on the image (String)
# @return:        Saves the image to 'slides' folder
# """
# def overlay_text_on_image(keyword, description):
#     img = Image.open(keyword+".jpg")
#     font = ImageFont.load("arial.pil")

#     # Find the image

