from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import cv2
import GetSlides
import vidtext

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
    gen_video(content)
    return send_file("project.mp4")


def gen_video(content):
    # Form description_map (same key/value for now)
    description_map = {sentence: sentence for sentence in content}
    # Call make_slides
    img_array = GetSlides.make_slides(description_map)
    # TODO: Turn image_arr into video
    # TODO: Figure out how to append audio from Jasper's work
    # TODO: Accept vs, size, and font from user
    vs = 0.1
    size = (1280, 720)
    out = cv2.VideoWriter('project.mp4', cv2.VideoWriter_fourcc(*'mp4v'), vs, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

