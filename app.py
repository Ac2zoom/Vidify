from flask import Flask, render_template, request, Response, send_file
import cv2
import GetSlides
import re
import os
import mimetypes
import nltk.data

app = Flask(__name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB


def summary(data):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return tokenizer.tokenize(data)


@app.route('/')
def index():
    # Form for source and text
    return render_template('index.html')


# Endpoint to handle keywords
@app.route("/vidify", methods=['GET', 'POST'])
def vidify():
    source_url = request.args.get('source')
    text = request.args.get('text')
    # TODO: Summarize text (use Rock's functions)
    content = summary(text)  # Return List
    gen_video(content)
    return render_template("video.html", source=source_url, video="/video/" + hex(hash(''.join(content))))


@app.route("/video/<vid_hash>", methods=['GET', 'POST'])
def video(vid_hash):
    return send_file('videos/' + vid_hash + '.mp4')


def gen_video(content):
    # Form description_map (same key/value for now)
    description_map = {sentence: sentence for sentence in content}
    # Call make_slides
    img_array = GetSlides.make_slides(description_map, hex(hash(''.join(content))))
    # Turn image_arr into video
    # TODO: Figure out how to append audio from Jasper's work
    # TODO: Accept vs, size, and font from user
    vs = 0.1
    size = (1280, 720)
    out = cv2.VideoWriter('videos/' + hex(hash(''.join(content))) + '.mp4', cv2.VideoWriter_fourcc(*'H264'), vs, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
