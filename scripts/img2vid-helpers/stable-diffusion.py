from os import getenv, path
import subprocess

def run(model, image):
    cfg_folder = getenv("CONFIG_FOLDER")
    runnum = getenv("runnum")

    subprocess.run(f"pip install {' '.join(model['packages'])} --extra-index-url {','.join(model['extra_indexes'])}", shell=True)
    
    import torch
    from diffusers import StableVideoDiffusionPipeline
    from diffusers.utils import load_image, export_to_video

    print('\nGenerating video', flush=True)
    print("| Using:", flush=True)
    print("Model: " + model["model"], flush=True)

    savepath = path.join(path.abspath(cfg_folder), 'img2vid', f"{runnum}.mp4")

    pipe = StableVideoDiffusionPipeline.from_pretrained(model["model"])

    # Load the conditioning image
    image = load_image(image)
    image = image.resize((1024, 576))

    frames = pipe(image, num_inference_steps=model["inference_count"]).frames[0]
    export_to_video(frames, savepath, fps=model["fps"])
    
    return savepath