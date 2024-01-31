from os import getenv, path, makedirs
from subprocess import run
import json, importlib, urllib.request
from io import BytesIO

cfg_folder = getenv("CONFIG_FOLDER")
ai = getenv("ai")
runnum = getenv("runnum")

with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
    config = json.load(file)

with open(path.join(cfg_folder, 'models.json'), 'r') as file:
    models = json.load(file)["img_upscale"] 

if config["txt2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{txt2img.out}", f'./txt2img/{runnum}'))
if config["img2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{img2img.out}", f'./img2img/{runnum}'))

config = config["img_upscale"]

run("pip install pillow~=10.2.0", shell=True)
from PIL import Image
try:
    image = Image.open(config["image"])
except:
    response = urllib.request.urlopen(path)
    data = response.read()
    image = Image.open(BytesIO(data))
    
makedirs(path.join(cfg_folder, "img_upscale"), exist_ok=True)
run(f"pip install {' '.join(models[ai]['packages'])} --extra-index-url {','.join(models[ai]['extra_indexes'])}", shell=True)

print('\nUsing helper: ' + models[ai]['helper'], flush=True)

helper = importlib.import_module(f"img_upscale-helpers.{models[ai]['helper']}")
path = helper.run(models[ai], image, config["scale"])

run(f'echo out={path} >> $GITHUB_OUTPUT', shell=True)
print(f'Generated image and saved to {path}')
