import os
import ast
from configparser import ConfigParser as CP

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

IMG_SIZE = ast.literal_eval(config.get("create_data","img_size"))

print(IMG_SIZE)