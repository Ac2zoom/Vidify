import vidtext

li = "Text"  # Text Content for video
content = vidtext.summary(li)  # Return List
vidtext.TextToVideo(content, vs=0.1)  # vs to control the speed of video
