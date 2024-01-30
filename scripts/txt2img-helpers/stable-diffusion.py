from sdkit.generate import generate_images
from sdkit.models import load_model
from sdkit.utils import save_images
import sdkit, urllib.request, glob
from tqdm import tqdm
from PIL import Image
from os import makedirs, path, getenv

def run(model, ctx, h, w):
    cfg_folder = getenv("CONFIG_FOLDER")

    print('\nGenerating image for question: ' + ctx, flush=True)
    print("| Using:", flush=True)
    print("Model from: " + model["dld_url"], flush=True)
    print("Dimensions: " + str(h) + "px x " + str(w) + "px", flush=True)

    makedirs("./tmp/x", exist_ok=True)
    ext=model["dld_url"].split(".")[-1]
    with urllib.request.urlopen(model["dld_url"]) as response, open('./tmp/'+"model."+ext, 'wb') as output_file:
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
    context.model_paths['stable-diffusion'] = './tmp/'+"model."+ext
    load_model(context, 'stable-diffusion')

    image = generate_images(context, width=int(w), height=int(h), prompt=ctx, seed=42, num_inference_steps=model["inference_count"])
    save_images(image, dir_path=path.join(cfg_folder, "txt2img"))

    savepath = path.join(path.abspath(cfg_folder), 'txt2img', '1.jpg')
    jpeg_image = Image.open(glob.glob(path.join(cfg_folder, 'txt2img', '*.jpeg'))[0])
    jpeg_image.save(savepath, format="JPEG")

    return savepath