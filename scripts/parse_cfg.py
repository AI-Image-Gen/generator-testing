from os import getenv, path
import urllib.request as web
import json, sys

settings_url = getenv("SETTINGS")
cfg_folder = getenv("CONFIG_FOLDER")

try:
    with open(path.join(cfg_folder, "settings.json"), 'r') as file:
        def_cfg = json.loads(file.read())
    with open(path.join(cfg_folder, "models.json"), 'r') as file:
        def_models = json.loads(file.read())

except (FileNotFoundError, json.JSONDecodeError):
    print("Error: Unable to get the default settings")
    sys.exit(1)

try:
    # Download JSON data from the URL
    response = web.urlopen(settings_url)
    data = response.read()

    # Load the JSON data
    settings_json = json.loads(data.decode('utf-8'))
    print("Settings file:")

except (web.error.URLError, json.JSONDecodeError):
    print("Error: Unable to fetch data from the URL.")

    settings_json = def_cfg
    print("Using default settings file:")

# Print JSON file
print(json.dumps(settings_json, indent=2))

# Define useful functions
def replace_models_in_string(mtype, string):
    models_names = list(def_models[mtype].keys())
    models_names_str = ', '.join(f'"{name}"' for name in models_names)
    return string.replace('"{type.models}"'.replace("type", mtype), f"[{models_names_str}]")
def search_json(data, target_string, exclude_key=None):
    if exclude_key is None:
        exclude_key = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key != exclude_key:
                if isinstance(value, (dict, list)):
                    if search_json(value, target_string, exclude_key):
                        return True
                elif isinstance(value, str) and target_string in value:
                    return True
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                if search_json(item, target_string, exclude_key):
                    return True
            elif isinstance(item, str) and target_string in item:
                return True
    return False
def process_integer_value(lower_limit, upper_limit, value, dividable=1):
    if not isinstance(value, int):
        value = lower_limit
    else:
        if value < lower_limit:
            value = lower_limit
        elif value > upper_limit:
            value = upper_limit
    while value % dividable != 0:
        value += 1
    return value
def process_type(variable, datatype):
    if not isinstance(variable, datatype):
            print(f"ERROR IN DEFAULT: {variable} is not proper value for field.")
            sys.exit(1)

# Process default config file

# Check var types
ints = [def_cfg["global"]["out_amount"], def_cfg["txt2img"]["height"], def_cfg["txt2img"]["width"], def_cfg["img2img"]["height"], def_cfg["img2img"]["width"], def_cfg["img_upscale"]["scale"]]
strs = [def_cfg["txt2txt"]["prompt"], def_cfg["txt2txt"]["prompt_pre"], def_cfg["txt2img"]["prompt"], def_cfg["img2img"]["prompt"], def_cfg["img2img"]["image"], def_cfg["img_upscale"]["image"], def_cfg["img2vid"]["prompt"], def_cfg["img2vid"]["image"]]
bools = [def_cfg["global"]["clean_artifacts"], def_cfg["txt2txt"]["active"], def_cfg["txt2txt"]["save_as_used"], def_cfg["txt2img"]["active"], def_cfg["img2img"]["active"], def_cfg["img_upscale"]["active"], def_cfg["img2vid"]["active"]]
for integer in ints: process_type(integer, int)
for string in strs: process_type(string, str)
for boolean in bools: process_type(boolean, bool)
# Integers values optimization
width_height_modules = [def_cfg["txt2img"], def_cfg["img2img"]]
for module in width_height_modules:
    module["width"] = process_integer_value(256, 1024, module["width"], 8)
    module["height"] = process_integer_value(256, 1024, module["height"], 8)
def_cfg["img_upscale"]["scale"] = process_integer_value(2, 4, def_cfg["img_upscale"]["scale"])
# Variable -> model type array
def_cfg_string = json.dumps(def_cfg)
model_types = ["txt2img", "img2img", "img_upscale", "img2vid"]
for model_type in model_types:
    def_cfg_string = replace_models_in_string(model_type, def_cfg_string)
def_cfg = json.loads(def_cfg_string)
# Check if variables used are proper
settings_types = model_types + ["txt2txt"]
for set_type in settings_types:
    if not def_cfg[set_type]["active"] and search_json(def_cfg, "{type.".replace("type", set_type), set_type):
        print(f"ERROR IN DEFAULT: Used {set_type} variable without turning on module")
        sys.exit(1)


# Process loaded config file

# Integers values optimization
width_height_modules = [settings_json["txt2img"], settings_json["img2img"]]
for module in width_height_modules:
    module["width"] = process_integer_value(256, 1024, module["width"], 8)
    module["height"] = process_integer_value(256, 1024, module["height"], 8)
settings_json["img_upscale"]["scale"] = process_integer_value(2, 4, settings_json["img_upscale"]["scale"])

# Variable -> model type array
settings_json_string = json.dumps(settings_json)
model_types = ["txt2img", "img2img", "img_upscale", "img2vid"]
for model_type in model_types:
    settings_json_string = replace_models_in_string(model_type, settings_json_string)
settings_json = json.loads(settings_json_string)

# Check if variables used are proper
settings_types = model_types + ["txt2txt"]
for set_type in settings_types:
    if not settings_json[set_type]["active"] and search_json(settings_json, "{type.".replace("type", set_type)):
        print(f"ERROR IN CUSTOM: Used {set_type} variable without turning on module")
        sys.exit(1)



json_string = json.dumps(settings_json)

model_types = ["txt2img", "img2img", "img_upscale", "img2vid"]
for model_type in model_types:
    json_string = push_models_to_json(model_type, json_string)


### MODULES ###

# -- Global --
if settings_json["global"]["clean_artifacts"] != True: 
    settings_json["global"]["clean_artifacts"] = False
settings_json["global"]["out_amount"] = process_integer_value(1, 10, settings_json["global"]["out_amount"])
if settings_json["global"]["push"] != True: 
    settings_json["global"]["push"] = False

# -- Txt2txt --
if settings_json["txt2txt"]["active"] != True: 
    settings_json["txt2txt"]["active"] = False
    settings_json["global"]["out_amount"] = 1
    # Variables
    if search_json(settings_json, "{txt2txt."):
        print("Error: Used txt2txt variable without module active")
        sys.exit(1)
else:
    if not settings_json["txt2txt"]["prompt_base"].strip(): 
        settings_json["txt2txt"]["prompt_base"] = def_cfg["txt2txt"]["prompt_base"]
    if not settings_json["txt2txt"]["prompt"].strip(): 
        settings_json["txt2txt"]["prompt"] = def_cfg["txt2txt"]["prompt"]
    if settings_json["txt2txt"]["save_as_used"] != True: 
        settings_json["txt2txt"]["save_as_used"] = False

# -- Txt2img --
if settings_json["txt2img"]["active"] != True: 
    settings_json["txt2img"]["active"] = False
    # Variables
    if search_json(settings_json, "{txt2img."):
        print("Error: Used txt2img variable without module active")
        sys.exit(1)
else:
    if not settings_json["txt2img"]["prompt"].strip(): 
        settings_json["txt2img"]["prompt"] = def_cfg["txt2img"]["prompt"]
    settings_json["txt2img"]["height"] = process_integer_value(256, 1024, settings_json["txt2img"]["height"], 8)
    settings_json["txt2img"]["width"] = process_integer_value(256, 1024, settings_json["txt2img"]["width"], 8)

    if settings_json["txt2img"]["matrix"]["models"]:
        models_array = settings_json["txt2img"]["matrix"]["models"]
    else:
        settings_json["txt2img"]["matrix"]["models"] = def_cfg[""]