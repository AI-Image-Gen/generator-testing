import json, sys, glob, subprocess
from tqdm import tqdm
from sdkit.generate import generate_images
from sdkit.models import load_model, unload_model
from sdkit.utils import save_images
import sdkit, urllib.request
from PIL import Image

if len(sys.argv) != 5:
    print("Json config file path, model name or dimensions are missing!")
    sys.exit(1)

with open('./prompt.txt', 'r') as file:
    prompt = file.read()

with open(sys.argv[1] + '/models.json', 'r') as file:
    data = json.load(file)
    model = data[sys.argv[2]]
    model["name"] = sys.argv[2]


print("| Using:")
print("Model: " + model["name"])

print("| With:")
print("Request: " + prompt)

if model["name"].endswith("online"):
    subprocess.run("pip install -U g4f~=0.2.0.3")
    subprocess.run(f'python ./online-providers/{model["name"]}.py "{prompt}"', shell=True)
    sys.exit()

print("Dimensions: " + str(sys.argv[3]) + "px x " + str(sys.argv[4]) + "px")
print("Downloaded from: " + model["repo_url"])
print("Inference count: " + str(model["inference_count"]))

context = sdkit.Context()
context.device = "cpu"

with urllib.request.urlopen(model["repo_url"]) as response, open('./tmp/'+model["name"]+"."+model["ext"], 'wb') as output_file:
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

context.model_paths['stable-diffusion'] = './tmp/'+model["name"]+"."+model["ext"]
load_model(context, 'stable-diffusion')

image = generate_images(context, width=int(sys.argv[3]), height=int(sys.argv[4]), prompt=prompt, seed=42, num_inference_steps=model["inference_count"])
save_images(image, dir_path="./tmp/image/")

unload_model(context, 'stable-diffusion')

jpeg_image = Image.open(glob.glob('./tmp/image/*.jpeg')[0])
jpeg_image.save("./tmp/image/1.jpg", format="JPEG")

print("Generated default image, starting upscaler...")