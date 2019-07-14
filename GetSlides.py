from google_images_download import google_images_download
from PIL import ImageFont, Image, ImageDraw
import cv2
import os


def make_slides(description_map):
    """
    Loops through all the given keywords and generates slides by
    finding images for the keywords and overlaying their descriptions onto the images.
    Saves the resulting images in the 'slides' folder
    @description_map:   a HashMap matching the keyword (String) with its description (String)
    @return:            Saves resulting slides to 'slides' folder
    """
    image_arr = []
    for keyword in description_map:
        get_image(keyword)
        description = description_map[keyword]
        image = overlay_text_on_image(keyword, description)
        image_arr.append(image)
    return image_arr


def get_image(keywords):
    """
    Finds all the images for the given keywords and downloads them into the downloads folder
    @keywords:  a comma separated list of keywords for images
    @return:    Saves the images to the downloads folder
    """
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords":keywords,
    # "suffix_keywords":"no watermark",
    "format":"jpg",
    "aspect_ratio":"wide",
    "usage_rights":"labeled-for-reuse-with-modifications",
    "limit":1,
    "size":"large",
    "print_urls":True}
    paths = response.download(arguments)

def overlay_text_on_image(keyword, description):
    # keyword = keyword + " no watermark"
    for file in os.listdir("downloads/" + keyword):
        filename = file
    
    font_style = "FancyHeartScript.ttf"
    font_size = 150
    font_placement = (50, 50)
    font_color = (255, 150, 150)


    img = Image.open("downloads/" + keyword + "/" + filename)
    # img = img.convert('RGB')

    img = img.resize((1280, 720), resample=0)
    draw = ImageDraw.Draw(img)

    # truetype(font.ttf, font-size)
    font = ImageFont.truetype(font_style, font_size)

    # text(position, text, color, font)
    draw.text(font_placement, description, fill=font_color, font=font)
    draw = ImageDraw.Draw(img)
    new_filename = "slides/" + keyword + ".png"
    img.save(new_filename)
    return cv2.imread(new_filename)
