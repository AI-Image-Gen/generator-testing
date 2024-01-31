from os import makedirs, path, getenv
import subprocess

def run(model, image, ctx, h, w):
    cfg_folder = getenv("CONFIG_FOLDER")
    runnum = getenv("runnum")

    subprocess.run(f"pip install {' '.join(model['packages'])} --extra-index-url {','.join(model['extra_indexes'])}", shell=True)

    from tqdm import tqdm
    from sdkit.generate import generate_images
    from sdkit.models import load_model
    from sdkit.filter import apply_filters
    import sdkit, urllib.request

    print('\Enhancing image with question: ' + ctx, flush=True)
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
    load_model(context, "nsfw_checker")

    image = generate_images(context, init_image=image, width=int(w), height=int(h), prompt=ctx, num_inference_steps=model["inference_count"])
    images_nsfw_filtered = apply_filters(context, "nsfw_checker", image)
    
    savepath = path.join(path.abspath(cfg_folder), 'txt2img', f'{runnum}.jpg')

    images_nsfw_filtered[0].save(savepath)

    return savepath