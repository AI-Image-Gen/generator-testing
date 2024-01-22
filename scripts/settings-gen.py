from os import getenv, path
from json import dumps, dump, load
from subprocess import run

PROMPT = getenv('PROMPT')
IS_IMAGE = getenv('IS_IMAGE').lower()
ENHANCE_PROMPT = getenv('ENHANCE_PROMPT').lower()
WIDTH = getenv('WIDTH')
HEIGHT = getenv('HEIGHT')
UPSCALE = getenv('UPSCALE').lower()
OUT_TYPE = getenv('OUT_TYPE').lower()
DISPATCHED_BY = getenv('DISPATCHED_BY').lower()
MULTIPLIER = getenv('MULTIPLIER')
CONFIG_FOLDER = getenv('CONFIG_FOLDER')

# Autonomous
if DISPATCHED_BY != 'workflow_dispatch':
    print('Autonomous mode on.')
    PROMPT=""
    IS_IMAGE="false"
    ENHANCE_PROMPT="true"
    WIDTH="768"
    HEIGHT="768"
    UPSCALE="3"
    OUT_TYPE="image"
    MULTIPLIER="1"

# Make values in range
def check_min_max(var1, minim, maxim):
    try:
        int_var = int(var1)
    except ValueError:
        int_var = 0
    if int_var < minim:
        int_var=minim
    elif int_var > maxim:
        int_var=maxim
    return int_var

MULTIPLIER = check_min_max(MULTIPLIER, 1, 10)
MULTIPLIER_ARRAY = dumps([i for i in range(MULTIPLIER)]).replace(" ", "")
HEIGHT = check_min_max(HEIGHT, 256, 1920)
WIDTH = check_min_max(WIDTH, 256, 1920)

txt2txt_gen = {'active': 'false', 'prompt': '', 'num': 1}
txt2img_gen = {'active': 'false', 'height': '768', 'width': '768', 'matrix': {'ai-models': [0], 'nums': [0]}}
img2img_gen = {'active': 'false', 'download-link': '', 'matrix': {'ai-models': [0], 'nums': [0], 'txt2img-ais': [0]}}
img_upscale_gen = {'active': 'false', 'download-link': '', 'upscale': '3', 'matrix': {'ai-models': [0], 'nums': [0], 'txt2img-ais': [0], 'img2img-ais': [0]}}
img2vid_gen = {'active': 'false', 'download-link': '', 'matrix': {'ai-models': [0], 'nums': [0], 'txt2img-ais': [0], 'img2img-ais': [0]}}

# List AI models
def get_model_list(models):
    models_list_tmp_1 = [model for model in models["online"].keys()]
    models_list_tmp_2 = [model for model in models["offline"].keys()]
    quoted_list = [f'"{element}"' for element in models_list_tmp_1 + models_list_tmp_2]
    models_list = dumps(quoted_list).replace(" ", "")
    return models_list

with open(path.join(CONFIG_FOLDER, 'models.json'), 'r') as file:
    data = load(file)

txt2img_AIs = get_model_list(data["txt2img"])
img2img_AIs = get_model_list(data["img2img"])
img2vid_AIs = get_model_list(data["img2vid"])
upscale_AIs = get_model_list(data["upscaler"])


#  Nice config generator

#   Enhancer, * => on
#   txt=>img: txt? => txt?* => img => img* =? upscaler
#   img=>img: img => img*/upscaler =? upscaler
#   img=>vid: img => img* => vid
#   txt=>vid: txt? => txt?* => img => img* => vid

# Prompt enhancer on
if ENHANCE_PROMPT == 'true':

    img2img_gen["active"] = 'true'
    img2img_gen["matrix"]["ai-models"] = img2img_AIs

    # Input => image
    if IS_IMAGE == 'true':
            
        img2img_gen["download-link"] = PROMPT

        # Output => video
        if OUT_TYPE == 'video':
            img2vid_gen["active"] = 'true'
            img2vid_gen["matrix"]["ai-models"] = img2vid_AIs
            img2vid_gen["matrix"]["img2img-ais"] = img2img_AIs

        # Output => image
        else:

            # Output upscale => not off
            if UPSCALE != 'off':
                img_upscale_gen["active"] = 'true'
                img_upscale_gen["upscale"] = UPSCALE
                img_upscale_gen["matrix"]["ai-models"] = upscale_AIs
                img_upscale_gen["matrix"]["img2img-ais"] = img2img_AIs

    # Input => normal prompt
    else:

        txt2txt_gen["active"] = 'true'
        txt2txt_gen["prompt"] = PROMPT
        txt2txt_gen["num"] = MULTIPLIER

        txt2img_gen['active'] = 'true'
        txt2img_gen['height'] = HEIGHT
        txt2img_gen['width'] = WIDTH
        txt2img_gen['matrix']["nums"] = MULTIPLIER_ARRAY
        txt2img_gen['matrix']["ai-models"] = txt2img_AIs

        img2img_gen["matrix"]["nums"] = MULTIPLIER_ARRAY
        img2img_gen["matrix"]["txt2img-ais"] = txt2img_AIs

        # Output => video
        if OUT_TYPE == 'video':
            img2vid_gen["active"] = 'true'
            img2vid_gen["matrix"]["nums"] = MULTIPLIER_ARRAY
            img2vid_gen["matrix"]["ai-models"] = img2vid_AIs
            img2vid_gen["matrix"]["txt2img-ais"] = txt2img_AIs
            img2vid_gen["matrix"]["img2img-ais"] = img2img_AIs

        # Output => image
        else:

            # Output upscale => not off
            if UPSCALE != 'off':
                img_upscale_gen["active"] = 'true'
                img_upscale_gen["upscale"] = UPSCALE
                img_upscale_gen["matrix"]["nums"] = MULTIPLIER_ARRAY
                img_upscale_gen["matrix"]["ai-models"] = upscale_AIs
                img_upscale_gen["matrix"]["txt2img-ais"] = txt2img_AIs
                img_upscale_gen["matrix"]["img2img-ais"] = img2img_AIs

# Prompt enhancer off
else:

    # Input => image
    if IS_IMAGE == 'true':

        # Output => video
        if OUT_TYPE == 'video':
            img2vid_gen["active"] == 'true'
            img2vid_gen["download-link"] = PROMPT
            img2vid_gen["matrix"]["ai-models"] = img2vid_AIs
    
        # Output => image
        else:
            
            # Bad request, define upscaler
            if UPSCALE == 'off':
                UPSCALE='2'

            img_upscale_gen["active"] = 'true'
            img_upscale_gen["upscale"] = UPSCALE
            img_upscale_gen["download-link"] = PROMPT
            img_upscale_gen["matrix"]["ai-models"] = upscale_AIs


    # Input => normal prompt
    else:

        # Bad request, tune input
        if not PROMPT.strip():
            txt2txt_gen["active"] = 'true'

        txt2img_gen['active'] = 'true'
        txt2img_gen['height'] = HEIGHT
        txt2img_gen['width'] = WIDTH
        txt2img_gen['matrix']["ai-models"] = txt2img_AIs

        # Output => video
        if OUT_TYPE == 'video':
            img2vid_gen["active"] = 'true'
            img2vid_gen["matrix"]["ai-models"] = img2vid_AIs
            img2vid_gen["matrix"]["txt2img-ais"] = txt2img_AIs

        # Output => image
        else:

            # Output upscale => not off
            if UPSCALE != 'off':
                img_upscale_gen["active"] = 'true'
                img_upscale_gen["upscale"] = UPSCALE
                img_upscale_gen["matrix"]["ai-models"] = upscale_AIs
                img_upscale_gen["matrix"]["txt2img-ais"] = txt2img_AIs


# Save generated config
settings = {'txt2txt': txt2txt_gen,'txt2img': txt2img_gen,'img2img': img2img_gen, 'img_upscale': img_upscale_gen, 'img2vid': img2vid_gen}
run(f"mkdir -p {path.join(CONFIG_FOLDER, 'tmp')}", shell=True, check=True)
with open(path.join(CONFIG_FOLDER, 'tmp', 'settings.json'), 'w') as file:
    dump(settings, file, indent=2)
settings_var = dumps(settings).replace(" ", "")
run(f'echo config={settings_var} >> $GITHUB_OUTPUT', shell=True)

print("Configuration for workflow set")