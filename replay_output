from osrparse import parse_replay_file
from PIL import Image, ImageDraw
import os

replay = parse_replay_file("/path/to/replay.osr")

length = 0

old_length = 0

events_to_use = []

for x in replay.play_data:
    length += x.time_since_previous_action

intervals = [x*17 for x in range(0, int(length/17))]

counter = 0
length = 0

for play in replay.play_data:
    length += play.time_since_previous_action
    if counter == len(intervals):
        break
    if length > intervals[counter]:
        counter += 1
        events_to_use.append(play)

frame_name = 0

for x in events_to_use:
    frame_name += 1
    image = Image.new('RGBA', (1920, 1080))
    draw = ImageDraw.Draw(image)
    draw.ellipse((int(x.x)*3.75, int(x.y)*3.75, (int(x.x)*3.75) + 5, (int(x.y)*3.75) + 5), fill='blue', outline='blue')
    image.save("osupics/{}.png".format(frame_name))
    
# made video with "ffmpeg -r 60 -f image2 -s 1920x1080 -i %d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4"
