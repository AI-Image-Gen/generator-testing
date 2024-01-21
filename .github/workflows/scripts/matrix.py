from os import path, getenv
from subprocess import run
from json import dumps, load

FAST_MODE = getenv('FAST_MODE')
RUNNERS_AMOUNT = getenv('RUNNERS_AMOUNT')
REPO_DIR = getenv('REPO_DIR')
CONFIG_FOLDER = getenv('CONFIG_FOLDER')
IS_IMAGE = getenv('IS_IMAGE')

try:
    int_runners_amount = int(RUNNERS_AMOUNT)
except ValueError:
    int_runners_amount = 0

if FAST_MODE.lower() == "true" or IS_IMAGE.lower() == "true" or int_runners_amount < 1:
    RUNNERS_AMOUNT=1
elif int_runners_amount > 10:
    RUNNERS_AMOUNT=10
    
json_array = [i for i in range(int_runners_amount)]
run_amount_array = dumps(json_array).replace(" ", "")

run(f'echo amount={run_amount_array} >> $GITHUB_OUTPUT', shell=True)

if IS_IMAGE.lower() == "false":
    with open(path.join(REPO_DIR, CONFIG_FOLDER, 'models.json'), 'r') as file:
        data = load(file)
        models = data["txt2img"]

else:
    with open(path.join(REPO_DIR, CONFIG_FOLDER, 'models.json'), 'r') as file:
        data = load(file)
        models = data["img2img"]

models_list_tmp = [model for model in models.keys()]
quoted_list = [f'"{element}"' for element in models_list_tmp]
models_list = dumps(quoted_list).replace(" ", "")

run(f'echo models={models_list  } >> $GITHUB_OUTPUT', shell=True)