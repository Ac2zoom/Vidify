from flask import Flask, render_template, request, send_file
import GetSlides
import os
import pollymode
from summarize import get_key_phrases
from pydub import AudioSegment
import os.path
from os import path

app = Flask(__name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB


@app.route('/')
def index():
    return render_template('page1.html')


@app.route('/assets/<path:subpath>')
def asset(subpath):
    return send_file('assets/' + subpath)


@app.route('/demo')
def demo():
    # Form for source and text
    return render_template('index.html')


# Endpoint to handle keywords
@app.route("/vidify", methods=['GET', 'POST'])
def vidify():
    source_url = request.form.get('source')
    text = request.form.get('text')
    # Summarize text
    # Return Tuple of Gensim Summarization and Comprehend_Phrases
    content = get_key_phrases(url_or_file=None, words=text)
    # TODO: Verify that this works given that each index of content[1] is a list
    vid_hash = hex(hash(str(content[1])))
    gen_video(content, vid_hash)
    return render_template("video.html", source=source_url, video="/video/" + vid_hash)


@app.route("/video/<vid_hash>", methods=['GET', 'POST'])
def video(vid_hash):
    return send_file('slides/' + vid_hash + '/output.mp4')


def gen_video(content, vid_hash):
    # Form description_map from summarize tuple
    sentence_list = content[0].split(".")
    # TODO: Add asserts/checks here to prevent errors
    description_map = {sentence_list[i]: content[1][i] for i in range(len(content[1]))}
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
    
    # Create file to build up reading sound
    sound = None
    # Create empty video file to build up video
    if not os.path.isdir("slides/" + vid_hash):
        os.mkdir("slides/" + vid_hash)

    # Loop through all sentences and create a recording for each one
    for i in range(min((5, len(sentence_list)))):
        synth = pollymode.PollySynth()
        speech = str(synth.mp3_speak("img" + str(i), sentence_list[i], None))
        # TODO: Get time to play file
        speech_temp = AudioSegment.from_mp3(speech)
        time = speech_temp.duration_seconds
        vs = 1 / time
        if path.exists("slides/video.mp4"):
            os.system("cd slides/" + vid_hash + "; ffmpeg -y -framerate " + str(vs) + " -i img-" + "{:02d}".format(i) +
                      ".png video2.mp4")
            os.system("cd slides/" + vid_hash +
                      "; printf \"file 'video.mp4'\nfile 'video2.mp4'\" > mylist.txt; ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy video.mp4")
        else:
            os.system("cd slides/" + vid_hash + "; ffmpeg -y -framerate " + str(vs) + " -i img-" + "{:02d}".format(i) +
                      ".png video.mp4")
        # Concatenate up a singular sound file
        if sound is None:
            sound = speech_temp
        else:
            sound += speech_temp
    # Build a singular sound file
    sound.export("slides/" + vid_hash + "/complete_reading.mp3", format="wav")

    # Merge sound and video file
    # videoMP4 = ffmpeg.input("cd slides/" + vid_hash + "/video.mp4")
    # audioMP3 = ffmpeg.input("complete_reading.mp3")
    # merged = ffmpeg.concat(videoMP4, audioMP3, v=1, a=1)
    # merged.output("cd slides/" + vid_hash + "/video2.mp4")
    # os.rename("slides/video2.mp4", "slides/video.mp4")
    # TODO: Revert back to equal framerate because more images
    # os.system("cd slides/" + vid_hash + "; ffmpeg -framerate " + str(vs) + " -i img-%02d.png video.mp4")
    os.system("cd slides/" + vid_hash + "; ffmpeg -y -i video.mp4 -i complete_reading.mp3 -c:v libx264 -c:a libvorbis -shortest output.mp4")
    # Not sure we need this here since output will create the final video
