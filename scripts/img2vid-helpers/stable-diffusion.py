from os import makedirs, getenv, path
import subprocess, urllib.request, importlib

def run(model, image):
    cfg_folder = getenv("CONFIG_FOLDER")
    runnum = getenv("runnum")

    subprocess.run(f"pip install {' '.join(model['packages'])} --extra-index-url {','.join(model['extra_indexes'])}", shell=True)

    from tqdm import tqdm
    from git import Repo
    
    print('\nGenerating video', flush=True)
    print("| Using:", flush=True)
    print("Model from: " + model["dld_url"], flush=True)

    # makedirs("./tmp/x", exist_ok=True)
    # ext=model["dld_url"].split(".")[-1]
    # with urllib.request.urlopen(model["dld_url"]) as response, open('./tmp/'+"model."+ext, 'wb') as output_file:
    #     print('Downloading [' + model["dld_url"] + "]...", flush=True)
    #     # Get the total file size in bytes
    #     file_size = int(response.getheader('Content-Length', 0))
    #     # Initialize the tqdm progress bar
    #     progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
    #     # Download and write to the local file with progress update
    #     while True:
    #         buffer = response.read(8192)  # Adjust the buffer size as needed
    #         if not buffer:
    #             break
    #         output_file.write(buffer)
    #         progress_bar.update(len(buffer))
    #     # Close the progress bar
    #     progress_bar.close()
    #     output_file.write(response.read())

    savepath = path.join(path.abspath(cfg_folder), 'img2vid')

    repo_url = 'https://github.com/Stability-AI/generative-models.git'
    Repo.clone_from(repo_url, path.join(cfg_folder, 'repo'))
    subprocess.run(f'mv {path.join(cfg_folder, "repo", "*")} .', shell=True)
    
    helper = importlib.import_module("scripts.sampling.simple_video_sample")
    helper.sample(image, version="svd_xt", device="cpu", output_folder=savepath)

    return savepath