from os import path, getenv
import subprocess

def run(model, ctx, h, w):
    cfg_folder = getenv("CONFIG_FOLDER")
    runnum = getenv("runnum")

    subprocess.run(f"pip install {' '.join(model['packages'])} --extra-index-url {','.join(model['extra_indexes'])}", shell=True)

    print('\nGenerating image for question: ' + ctx, flush=True)
    print("| Using:", flush=True)
    print("Model: " + model["model"], flush=True)
    print("With faster generation with: " + model["latent-consistency"], flush=True)
    print("Dimensions: " + str(h) + "px x " + str(w) + "px", flush=True)

    savepath = path.join(path.abspath(cfg_folder), 'txt2img', f'{runnum}.jpg')

    from diffusers import LCMScheduler, AutoPipelineForText2Image
    import torch

    pipe = AutoPipelineForText2Image.from_pretrained(model["model"], torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    # load and fuse lcm lora
    pipe.load_lora_weights(model["adapter"])
    pipe.fuse_lora()
    pipe.enable_model_cpu_offload()
    generator = torch.Generator(device="cpu")

    image = pipe(prompt=ctx, num_inference_steps=model["inference_count"], height=h, width=w, generator=generator, guidance_scale=0).images[0]
    image.save(savepath)

    return savepath