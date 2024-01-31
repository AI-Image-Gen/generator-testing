from os import getenv, path, makedirs
from subprocess import run
from io import BytesIO
import json, importlib, urllib.request

cfg_folder = getenv("CONFIG_FOLDER")
ai = getenv("ai")
runnum = getenv("runnum")

with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
    config = json.load(file)

with open(path.join(cfg_folder, 'models.json'), 'r') as file:
    models = json.load(file)["upscale"] 

if config["txt2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{txt2img.out}", path.join(cfg_folder, 'txt2img', f'{runnum}.jpg')))
if config["img2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{img2img.out}", path.join(cfg_folder, 'img2img', f'{runnum}.jpg')))

config = config["upscale"]

run("pip install pillow~=10.2.0", shell=True)
from PIL import Image
try:
    image = Image.open(config["input"])
except:
    response = urllib.request.urlopen(config["input"])
    data = response.read()
    image = Image.open(BytesIO(data))

image.save('tmp.jpg')
    
makedirs(path.join(cfg_folder, "upscale"), exist_ok=True)

print('\nUsing helper: ' + models[ai]['helper'], flush=True)

helper = importlib.import_module(f"img_upscale-helpers.{models[ai]['helper']}")
path = helper.run(models[ai], 'tmp.jpg', config["scale"])

run(f'echo out={path} >> $GITHUB_OUTPUT', shell=True)
print(f'Generated image and saved to {path}')
