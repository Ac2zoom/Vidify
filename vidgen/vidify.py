import vidtext

li = "Video Rocks"  # Text Content for video
# TODO: Replace this with Rock's method
content = vidtext.summary(li)  # Return List
print("Generating images for each of: " + str(content))
vidtext.TextToVideo(content, vs=0.1)  # vs to control the speed of video
