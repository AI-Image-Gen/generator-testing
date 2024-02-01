from os import path, getenv
import subprocess

def run(model, pass_img, ctx, w, h):
    cfg_folder = getenv("CONFIG_FOLDER")
    runnum = getenv("runnum")

    subprocess.run(f"pip install {' '.join(model['packages'])} --extra-index-url {','.join(model['extra_indexes'])}", shell=True)

    print('\nEnhancing image with prompt: ' + ctx, flush=True)
    print("| Using:", flush=True)
    print("Model: " + model["model"], flush=True)
    print("Dimensions: " + str(w) + "px x " + str(h) + "px", flush=True)

    savepath = path.join(path.abspath(cfg_folder), 'img2img', f'{runnum}.jpg')

    from diffusers import AutoPipelineForImage2Image
    from diffusers.utils import load_image

    init_img = load_image(pass_img)
    init_img = init_img.resize((w, h))
    pipe = AutoPipelineForImage2Image.from_pretrained(model["model"])

    image = pipe(prompt=ctx, image=init_img, num_inference_steps=model["inference_count"], height=h, width=w).images[0]
    image.save(savepath)

    return savepath