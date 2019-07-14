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
    """
    Finds the image associated with that keyword and overlays the description over the top of it
    @keyword:       The title of the image that needs a description (String)
    @description:   Short sentence to overlay on the image (String)
    @return:        Saves the image to 'slides' folder
    """
    # keyword = keyword + " no watermark"
    for file in os.listdir("downloads/" + keyword):
        filename = file
    
    font_style = "HelveticaNeue Medium.ttf"
    font_size = 50
    font_placement = (50, 50)
    font_color = (250, 250, 250)
    background_color = (0, 0, 0)
    background_size = get_back_size(description)


    img = Image.open("downloads/" + keyword + "/" + filename)
    # img = img.convert('RGB')

    img = img.resize((1280, 720), resample=0)
    draw = ImageDraw.Draw(img)

    # truetype(font.ttf, font-size)
    font = ImageFont.truetype(font_style, font_size)

    # text(position, text, color, font)
    draw.rectangle(((25,35), background_size), fill='black')
    draw.text(font_placement, description, fill=font_color, font=font)
    draw = ImageDraw.Draw(img)
    new_filename = "slides/" + keyword + ".png"
    img.save(new_filename)
    return cv2.imread(new_filename)

def get_back_size(description):
    line_count = 125
    lines = description.split('\n')
    length = len(max(lines, key=len))
    for char in description:
        if char == '\n':
            line_count += 60
            
    # length = len(description)
    if length == 0:
        return (25, 35)
    else:
        return (length*29, line_count)
