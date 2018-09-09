import osrparse
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

# replay = parse_replay_file("understand.osr")

with open("superdriver.osr", "rb") as f:
    data = f.read()

osu = Map("superdriver.osu")


replay = osrparse.parse_replay(data)

length1 = 0

events_to_use = []

intervals = [int(x*(1000/60)) for x in range(0, int(replay.play_data[-1].timestamp/(1000/60)))]

print(sorted(osu.hitobjects.keys())[-1])
print(replay.play_data[-1].timestamp)
print(len(replay.play_data))

plays = {}
for x in replay.play_data:
    plays[x.timestamp] = [x.x, x.y, x.keys_pressed]

frame_name = 0

height = 720
width = 1280

mod = height/384

buttons = {0: 'white', 1: 'grey', 2: 'yellow', 5: 'blue', 10: 'purple', 15: 'green', 16: 'black'}

font = ImageFont.truetype("path/to/font", 20)

currently_showing = []

circle_size = 32 * (1 - 0.7 * (osu.difficulty.circle_size - 5) / 5)

for mil in range(replay.play_data[0].timestamp, replay.play_data[-1].timestamp):
    try:
        currently_showing.append(osu.hitobjects[mil+600])
    except KeyError:
        pass
    except Exception as e:
        print(e)
        
    for x in currently_showing:
        if mil - x.time + 600 > 599:
            del currently_showing[currently_showing.index(x)]

    try:
        event = plays[mil]
    except KeyError:
        pass
    except Exception as e:
        print(e)
        
    if mil in intervals:
        frame_name += 1
        """
        image = Image.new('RGBA', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), (width, height)), fill='white', outline='white')"""
        for x in currently_showing:
            if x.type == 2 or x.type == 6:
                if x.slider_type == "L":
                    x_coord = np.array([x.x] + [int(cord[0]) for cord in x.curve_points[0]])
                    y_coord = np.array([x.y] + [int(cord[1]) for cord in x.curve_points[0]])
                    z = np.polyfit(x_coord, y_coord, len(x.curve_points[0])).tolist()
                    start = min(int(x.curve_points[0][0][0]), x.x)
                    end = max(int(x.curve_points[0][0][0]), x.x)
                    for point in range(start, end):
                        pass
 #                       draw.ellipse((point * mod - circle_size, (m*point + c) * mod - circle_size, point * mod + circle_size, (m*point + c) * mod + circle_size), fill='red', outline='red')
                elif x.slider_type == "B":
                    print("{}:{}".format(x.x, x.y))
                    print(x.curve_points)
                
                else:
                    pass
 #                   draw.ellipse((x.x * mod - circle_size, x.y * mod - circle_size, x.x * mod + circle_size, x.y * mod + circle_size), fill='red', outline='red')
                        
                    #print(x.slider_type)
                    #print("{}:{}, {}".format(x.x, x.y, ", ".join(["{}:{}".format(point[0], point[1]) for point in x.curve_points.values()])))
            else:
                pass
"""               draw.ellipse((x.x * mod - circle_size, x.y * mod - circle_size, x.x * mod + circle_size, x.y * mod + circle_size), fill='red', outline='red')
        draw.ellipse((int(event[0])*mod, int(event[1])*mod, (int(event[0])*mod) + 20, (int(event[1])*mod) + 20), fill='blue', outline='blue')
        draw.rectangle(((100, 100), (150, 150)), fill=buttons[event[2]], outline='black')
        draw.text((100, 180), "{}".format(frame_name), fill="black", font=font)
        image.save("osupics/{}.png".format(frame_name))"""
