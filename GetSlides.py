from google_images_download import google_images_download
from PIL import ImageFont, Image, ImageDraw
import os


def make_slides(description_map, vid_hash):
    """
    Loops through all the given keywords and generates slides by
    finding images for the keywords and overlaying their descriptions onto the images.
    Saves the resulting images in the 'slides' folder
    @description_map:   a HashMap matching the keyword (String) with its description (String)
    @return:            Saves resulting slides to 'slides' folder
    """
    image_arr = []
    count = 0
    for description in description_map:
        print("Description: " + str(description))
        if count > 5:
            break
        # This assumes that description's value is a list
        keywords = " ".join(description_map[description])
        if keywords is "":
            continue
        image_path = get_image(keywords)
        print(image_path)
        image = overlay_text_on_image(image_path[0][list(image_path[0].keys())[0]][0], description, vid_hash, count)
        image_arr.append(image)
        count += 1
    return image_arr


def get_image(keywords):
    """
    Finds all the images for the given keywords and downloads them into the downloads folder
    @keywords:  a comma separated list of keywords for images
    @return:    Saves the images to the downloads folder
    """
    print("Keywords: " + keywords)
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keywords,
        # "suffix_keywords":"no watermark",
        "format": "jpg",
        "aspect_ratio": "wide",
        "usage_rights": "labeled-for-reuse-with-modifications",
        "limit": 1,
        "size": "large",
        "print_urls": True}
    return response.download(arguments)


def overlay_text_on_image(filename, description, vid_hash, count):
    """
    Finds the image associated with that keyword and overlays the description over the top of it
    @keyword:       The title of the image that needs a description (String)
    @description:   Short sentence to overlay on the image (String)
    @return:        Saves the image to 'slides' folder
    """
    # truetype(font.ttf, font-size)
    font_style = "HelveticaNeue Medium.ttf"
    font_size = 30
    font_placement = (50, 50)
    
    # (R, G, B)
    font_color = (250, 250, 250)
    background_color = (0, 0, 0)
    img = Image.open(filename)

    img = img.resize((1280, 720), resample=0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_style, font_size)
    
    description = insert_newline(description, font_size)
    background_size = get_back_size(description, font_size, draw, font)

    # fill = background color
    draw.rectangle(((25,35), background_size), fill='black')

    # text(position, text, color, font)
    draw.text(font_placement, description, font_color, font=font)
    draw = ImageDraw.Draw(img)
    # If no vid_hash directory, create one
    dir_path = "slides\\" + vid_hash
    if not os.path.isdir("slides"):
        os.mkdir("slides")
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    new_filename = dir_path + "\\img-" + "{:02d}".format(count) + ".png"
    img.save(new_filename)

    return new_filename


def get_back_size(description, font_size, draw, font):
    length = draw.textsize(description, font)
    return_length = (length[0] + 80, length[1] + 70)
    if len(description) == 0:
        return 25, 35
    else:
        return return_length


def insert_newline(description, font_size):
    char_count = 0
    words = ''.join(description).split(' ')
    for i in range(len(words)):
        char_count += len(words[i]) + 1
        if (char_count * (int)(font_size * (0.5))) > 1200:
            words.insert(i, '\n')
            i += 1
            char_count = 0
    
    return ' '.join(words)
