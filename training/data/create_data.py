import os
import ast
import random
from tqdm import tqdm # for progress bar visualization
from configparser import ConfigParser as CP
from PIL import Image

############################# LOAD CONFIG #############################

config = CP()
config.read(os.path.join(os.getcwd(),"etc",".conf"))

IMG_SIZE = ast.literal_eval(config.get("create_data","img_size"))
N_SAMPLES = ast.literal_eval(config.get("create_data","number_of_samples"))
DATASET_VERSION = config.get("create_data","dataset_version")
N_SHAPES = ast.literal_eval(config.get("create_data","number_of_shapes_per_img")) # tuple with min and max
RANDOM_ROTATION = ast.literal_eval(config.get("create_data","random_rotation"))

########################### GENERATE IMAGES ###########################

def generate_image(out_dir:str,templates_dir:str,uid=1)->None:
    '''paste a number of templates onto a whilte image to generate a training image; specify details in .conf under "create_data"'''
    image = Image.new("RGBA", IMG_SIZE,"white")

    all_templates =[f"{d}/{i}.png" for d in os.listdir(templates_dir) for i in range(len(os.listdir(os.path.join(templates_dir,os.listdir(templates_dir)[0]))))]
    templates = random.choices(all_templates,k=random.randint(*N_SHAPES))
    for file in templates:
        template = Image.open(os.path.join(templates_dir,file)).convert("RGBA")
        if RANDOM_ROTATION:
            angle = random.uniform(0,360)
            template = template.rotate(angle,expand=True)
            x_h = min(IMG_SIZE[0]-1,int(template.size[0]*random.uniform(0.5,1.5)))
            y_h = min(IMG_SIZE[1]-1,int(template.size[1]*random.uniform(0.5,1.5)))
            template = template.resize((x_h,y_h))
        position = [random.randint(0,a-b) for a,b in zip(IMG_SIZE,template.size)] # pick random position inside the image
        image.paste(template,position,template) # use template as its own mask, to dicard transparent pixels

    # ensure directory for dataset version exists
    if not(os.path.isdir(out_dir)):
        os.mkdir(out_dir)
    image.save(os.path.join(out_dir,f"{uid}.png"))
    

if __name__ == "__main__":
    
    dt_path = "training/data"
    
    out_path = os.path.join(os.getcwd(),dt_path,"training_data",DATASET_VERSION)
    template_path = os.path.join(os.getcwd(),dt_path,"templates/templates")
    
    for i in tqdm(range(N_SAMPLES), f"generating new dataset ({DATASET_VERSION})"):
        generate_image(out_path,template_path,i)
