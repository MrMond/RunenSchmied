'''define paths in template_shapes.json as a list of points (rang: [0;1]) and execute this script to generate some templates'''

import json
import os
import ast
from configparser import ConfigParser as CP
from PIL import Image, ImageDraw

CD = os.path.dirname(os.path.abspath(__file__))

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

IMG_SIZE = ast.literal_eval(config.get("template","img_size"))
LINE_WIDTH = ast.literal_eval(config.get("template","line_width"))

with open(os.path.join(CD,"template_shapes.json"),"r") as of:
    template_definitions = json.load(of)

for key, trail in template_definitions.items():

    name = f"{key}.png"
    color = trail['color']
    path = trail['path']
    path = [(int(p[0]*IMG_SIZE[0]),int(p[1]*IMG_SIZE[1])) for p in path] # scale path to IMG_SIZE

    print(f"{name}\t{color}\t\t{path}")

    img = Image.new("RGBA",IMG_SIZE,"#FFFFFF00")

    draw = ImageDraw.Draw(img)
    draw.line(path,fill=color,width=LINE_WIDTH)

    img.save(os.path.join(CD,"templates",name), compress_level=0)
    img.close()