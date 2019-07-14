from flask import Flask, render_template, request, send_file
import GetSlides
import os
import pollymode
from summarize import get_key_phrases
from pydub import AudioSegment
import ffmpeg

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
    source_url = request.args.get('source')
    text = request.args.get('text')
    # Summarize text
    content = get_key_phrases(text)  # Return Tuple of Gensim Summarization and Comprehend_Phrases
    # TODO: Verify that this works given that each index of content[1] is a list
    vid_hash = hex(hash(''.join(content[1])))
    gen_video(content, vid_hash)
    return render_template("video.html", source=source_url, video="/video/" + vid_hash)


@app.route("/video/<vid_hash>", methods=['GET', 'POST'])
def video(vid_hash):
    return send_file('slides/' + vid_hash + '/video.mp4')


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
    sound = AudioSegment()
    # Create empty video file to build up video
    open("cd slides/" + vid_hash + 'video.mp4', 'a').close()

    # Loop through all sentences and create a recording for each one
    for i in range(len(sentence_list)):
        synth = pollymode.PollySynth()
        speech = synth.mp3_speak("img" + str(i), sentence_list[i], None)
        # TODO: Get time to play file
        speech_temp = AudioSegment.from_mp3(speech)
        time = speech_temp.duration_seconds
        vs = 1 / time

        os.system("cd slides/" + vid_hash + "; ffmpeg - framerate " + str(vs) + " -i img-" + str(i) + ".png video2.mp4")
        os.system("cd slides/" + vid_hash + ";ffmpeg -i “concat:video.mp4|video2.mp4” video.mp4")
        # Concatenate up a singular sound file
        sound += speech
    # Build a singular sound file
    sound.export("complete_reading.mp3", format="mp3")

    # Merge sound and video file
    videoMP4 = ffmpeg.input("cd slides/" + vid_hash + "/video.mp4")
    audioMP3 = ffmpeg.input("complete_reading.mp3")
    merged = ffmpeg.concat(videoMP4, audioMP3, v=1, a=1)
    output = ffmpeg.output(merged[0], merged[1], "video.mp4")

    # Not sure we need this here since output will create the final video
    # os.system("cd slides/" + vid_hash + "; ffmpeg -framerate " + str(vs) + " -i img-%02d.png video.mp4")
