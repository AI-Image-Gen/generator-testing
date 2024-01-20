import json, sys, urllib.request, subprocess
from tqdm import tqdm

if len(sys.argv) != 2:
    print("Json config file path missing!")
    sys.exit(1)

with open(sys.argv[1] + '/models.json', 'r') as file:
    data = json.load(file)
    model = data['upscaler']

with urllib.request.urlopen(model["repo_url"]) as response, open('./tmp/model.pth', 'wb') as output_file:
    print('Downloading [' + model["repo_url"] + "]...")
     # Get the total file size in bytes
    file_size = int(response.getheader('Content-Length', 0))
    # Initialize the tqdm progress bar
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
    # Download and write to the local file with progress update
    while True:
        buffer = response.read(8192)  # Adjust the buffer size as needed
        if not buffer:
            break
        output_file.write(buffer)
        progress_bar.update(len(buffer))

    # Close the progress bar
    progress_bar.close()
    output_file.write(response.read())

with urllib.request.urlopen(model["inference_script"]) as response, open('./tmp/inference_script.py', 'wb') as output_file:
    print('Downloading [' + model["inference_script"] + "]...")
     # Get the total file size in bytes
    file_size = int(response.getheader('Content-Length', 0))
    # Initialize the tqdm progress bar
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
    # Download and write to the local file with progress update
    while True:
        buffer = response.read(8192)  # Adjust the buffer size as needed
        if not buffer:
            break
        output_file.write(buffer)
        progress_bar.update(len(buffer))

    # Close the progress bar
    progress_bar.close()
    output_file.write(response.read())

print("| Starting downloaded script...")

print("From: " + model["inference_script"])
print("Using downloaded model: " + model["repo_url"])