from os import getenv, path, makedirs, remove
from subprocess import run
import json, importlib

cfg_folder = getenv("CONFIG_FOLDER")
ai = getenv("ai")
runnum = getenv("runnum")

with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
    config = json.load(file)

with open(path.join(cfg_folder, 'models.json'), 'r') as file:
    models = json.load(file)["img2vid"] 

if config["txt2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{txt2img.out}", path.join(cfg_folder, 'txt2img', f'{runnum}.jpg')))
if config["img2img"]["active"]:
    config = json.loads(json.dumps(config).replace("{img2img.out}", path.join(cfg_folder, 'img2img', f'{runnum}.jpg')))

config = config["img2vid"]
    
makedirs(path.join(cfg_folder, "img2vid"), exist_ok=True)

print('\nUsing helper: ' + models[ai]['helper'], flush=True)

helper = importlib.import_module(f"img2vid-helpers.{models[ai]['helper']}")
path = helper.run(models[ai], config["image"], config["gif"], config["video"])

if config["video"]["music"] and config["video"]["enable"]:
    helper = importlib.import_module(f"img2vid-helpers.img2txt.{models[ai]['img2txt']['helper']}")
    prompt = helper.run(models[ai]['img2txt']['model'], config["image"])

    helper = importlib.import_module(f"img2vid-helpers.music.{models[ai]['music']['helper']}")
    musicfile_path = helper.run(models[ai]['music']["model"], prompt)

    from moviepy.editor import VideoFileClip, AudioFileClip
    video_clip = VideoFileClip(path.join(path,f"{runnum}.mp4"))
    audio_clip = AudioFileClip(musicfile_path)
    video_clip = video_clip.set_audio(audio_clip)
    remove(path.join(path,f"{runnum}.mp4"))
    video_clip.write_videofile(path.join(path,f"{runnum}.mp4"))

run(f'echo out={path} >> $GITHUB_OUTPUT', shell=True)
print(f'Generated video and saved to {path}')
