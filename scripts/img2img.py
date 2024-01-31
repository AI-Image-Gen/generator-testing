from os import getenv, path, makedirs
from subprocess import run
import json, importlib, urllib.request
from io import BytesIO

cfg_folder = getenv("CONFIG_FOLDER")
ai = getenv("ai")
num = getenv("num")
runnum = getenv("runnum")

with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
    config = json.load(file)

with open(path.join(cfg_folder, 'models.json'), 'r') as file:
    models = json.load(file)["img2img"] 

if config["txt2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{txt2img.out}", path.join(cfg_folder, 'txt2img', f'{runnum}.jpg')))
if config["txt2txt"]["active"]:
    txt2txt = json.loads(getenv("txt2txt").replace('*', ' '))
    config = json.loads(json.dumps(config).replace("{txt2txt.out}", txt2txt[num]))
config = config["img2img"]

run("pip install pillow~=10.2.0", shell=True)
from PIL import Image
try:
    image = Image.open(config["image"])
except:
    response = urllib.request.urlopen(path)
    data = response.read()
    image = Image.open(BytesIO(data))

image.save('tmp.jpg')
    
makedirs(path.join(cfg_folder, "img2img"), exist_ok=True)

print('\nUsing helper: ' + models[ai]['helper'], flush=True)

helper = importlib.import_module(f"img2img-helpers.{models[ai]['helper']}")
path = helper.run(models[ai], 'tmp.jpg', config["prompt"], config["height"], config["width"])

run(f'echo out={path} >> $GITHUB_OUTPUT', shell=True)
print(f'Generated image and saved to {path}')
