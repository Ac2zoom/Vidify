from flask import Flask, render_template, request, Response
import cv2
import GetSlides
import vidtext
import re
import os
import mimetypes

app = Flask(__name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB


@app.route('/')
def hello_world():
    # Form for source and text
    return render_template('index.html')


# Endpoint to handle keywords
@app.route("/vidify", methods=['GET', 'POST'])
def vidify():
    source_url = request.args.get('source')
    text = request.args.get('text')
    # TODO: Summarize text (use Rock's functions)
    content = vidtext.summary(text)  # Return List
    gen_video(content)
    return render_template("video.html", source=source_url, video="/video/" + hex(hash(''.join(content))))


@app.route("/video/<vid_hash>", methods=['GET', 'POST'])
def video(vid_hash):
    path = 'videos/' + vid_hash + '.mp4'

    start, end = get_range(request)
    return partial_response(path, start, end)


def partial_response(path, start, end=None):
    global BUFF_SIZE
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    return response


def get_range(request):
    range = request.headers.get('Range')
    print(request.headers)
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        print(start, end)
        return start, end
    else:
        return 0, None


def gen_video(content):
    # Form description_map (same key/value for now)
    description_map = {sentence: sentence for sentence in content}
    # Call make_slides
    img_array = GetSlides.make_slides(description_map)
    # Turn image_arr into video
    # TODO: Figure out how to append audio from Jasper's work
    # TODO: Accept vs, size, and font from user
    vs = 0.1
    size = (1280, 720)
    out = cv2.VideoWriter('videos/' + hex(hash(''.join(content))) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), vs, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

