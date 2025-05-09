from configparser import ConfigParser as CP
from PIL import Image
import os
import ast

import random

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

MODEL_VERSION = config.get("game","model_version")
MODEL_PATH = os.path.join(os.getcwd(),"training/model/models",f"{MODEL_VERSION}.pth")# map each template to a stat of the character
TERMPLATE_PATH = os.path.join(os.getcwd(),"training/data/templates/templates")
STAT_MAP = ast.literal_eval(config.get("game","template_stat_match"))

def get_stats_from_image(img:Image)->dict:
    templates = [t.split(".")[0] for t in os.listdir(TERMPLATE_PATH)]
    d = {STAT_MAP[t]:random.randint(0,10) for t in templates}
    return d

if __name__ == "__main__":
    print(get_stats_from_image(None))