from flask import Flask, render_template, request, send_file
import GetSlides
import os
import nltk.data

app = Flask(__name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB


# TODO: Replace with call to Rock's work (summarize.py)
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
    vid_hash = hex(hash(''.join(content)))
    gen_video(content, vid_hash)
    return render_template("video.html", source=source_url, video="/video/" + vid_hash)


@app.route("/video/<vid_hash>", methods=['GET', 'POST'])
def video(vid_hash):
    return send_file('slides/' + vid_hash + '/video.mp4')


def gen_video(content, vid_hash):
    # Form description_map (same key/value for now)
    description_map = {sentence: sentence for sentence in content}
    # Call make_slides
    # TODO: cv2 references aren't necessary anymore
    img_array = GetSlides.make_slides(description_map, vid_hash)
    # Turn image_arr into video
    # TODO: Figure out how to append audio from Jasper's work
    # ffmpeg -i video.mp4 -i audio.mp3 -codec copy -shortest output.mp4
    # TODO: Accept vs, size, intro, and font from user
    vs = 0.2
    # size = (1280, 720)
    # TODO: Switch to using ffmpeg-python
    os.system("cd slides/" + vid_hash + "; ffmpeg -framerate " + str(vs) + " -i img-%02d.png video.mp4")
