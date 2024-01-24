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

