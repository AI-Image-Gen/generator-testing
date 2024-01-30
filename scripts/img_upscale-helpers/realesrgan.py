from sdkit.filter import apply_filters
from sdkit.models import load_model
import sdkit, urllib.request, glob
from tqdm import tqdm
from PIL import Image
from os import makedirs, path, getenv

def run(model, image, scale):
    cfg_folder = getenv("CONFIG_FOLDER")

    print('\nUpscaling image by ' + scale + 'x', flush=True)
    print("| Using:", flush=True)
    print("Model from: " + model["dld_url"], flush=True)

    makedirs("./tmp/x", exist_ok=True)
    with urllib.request.urlopen(model["dld_url"]) as response, open('./tmp/'+"model.xd", 'wb') as output_file:
        print('Downloading [' + model["dld_url"] + "]...", flush=True)
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

    context = sdkit.Context()
    context.device = "cpu"
    context.model_paths['realesrgan'] = './tmp/'+"model.xd"
    load_model(context, 'realesrgan')

    image_upscaled = apply_filters(context, "realesrgan", image, scale=scale)   
        
    savepath = path.join(path.abspath(cfg_folder), 'img_upscale', '1.jpg')

    image_upscaled.save(savepath)

    return savepath