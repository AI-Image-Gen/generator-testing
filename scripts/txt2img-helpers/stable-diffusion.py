from os import path, getenv
import subprocess

def run(model, ctx, w, h):
    cfg_folder = getenv("CONFIG_FOLDER")
    runnum = getenv("runnum")

    subprocess.run(f"pip install {' '.join(model['packages'])} --extra-index-url {','.join(model['extra_indexes'])}", shell=True)

    print('\nGenerating image for question: ' + ctx, flush=True)
    print("| Using:", flush=True)
    print("Model: " + model["model"], flush=True)
    print("Dimensions: " + str(w) + "px x " + str(h) + "px", flush=True)

    savepath = path.join(path.abspath(cfg_folder), 'txt2img', f'{runnum}.jpg')

    from diffusers import AutoPipelineForText2Image

    pipe = AutoPipelineForText2Image.from_pretrained(model["model"])

    image = pipe(prompt=ctx, num_inference_steps=model["inference_count"], height=h, width=w).images[0]
    image.save(savepath)

    return savepath