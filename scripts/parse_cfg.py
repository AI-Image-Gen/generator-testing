from os import getenv, path
import urllib.request as web
import json, sys

settings_url = getenv("SETTINGS")
cfg_folder = getenv("CONFIG_FOLDER")

try:
    # Download JSON data from the URL
    response = web.urlopen(settings_url)
    data = response.read()

    # Load the JSON data
    settings_json = json.loads(data.decode('utf-8'))
    print("Settings file:")

except (web.error.URLError, json.JSONDecodeError):
    print("Error: Unable to fetch data from the URL.")
    try:

        # Open the file in read mode
        with open(path.join(cfg_folder, "settings.json"), 'r') as file:

            # Load the JSON data
            settings_json = json.loads(file.read())
            print("Using default settings file:")
        
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Unable to fallback to default json")
        sys.exit(1)


# Print JSON file
print(json.dumps(settings_json, indent=2))

def search_json(data, target_string):
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, (dict, list)):
                if search_json(value, target_string):
                    return True
            elif isinstance(value, str) and target_string in value:
                return True
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                if search_json(item, target_string):
                    return True
            elif isinstance(item, str) and target_string in item:
                return True
    return False
def process_integer_value(lower_limit, upper_limit, value):
    if not isinstance(value, int):
        value = lower_limit
    else:
        if value < lower_limit:
            value = lower_limit
        elif value > upper_limit:
            value = upper_limit
    return value

### VARIABLES ###

# -- txt2txt --
# If module off
if settings_json["txt2txt"]["active"] != True:
    settings_json["txt2txt"]["active"] = False
    # Used variable without module on
    if search_json(settings_json, "{txt2txt."):
        print("Error: Used txt2txt variable without module active")
        sys.exit(1)
    # Set global.out_amount when is not active
    settings_json["global"]["out_amount"] = 1



### MODULES ###

# -- Global --
# Stabilize global.clean_artifacts value
if settings_json["global"]["clean_artifacts"] != True: settings_json["global"]["clean_artifacts"] = False
# Stabilize global.out_amount value
settings_json["global"]["out_amount"] = process_integer_value(1, 10, settings_json["global"]["out_amount"])
# Stabilize global.push value
if settings_json["global"]["push"] != True: settings_json["global"]["push"] = False

