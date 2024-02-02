from transformers import pipeline
from os import getenv, path
import scipy

def get_valid_prompt(text: str) -> str:
  dot_split = text.split('.')[0]
  n_split = text.split('\n')[0]

  return {
    len(dot_split) < len(n_split): dot_split,
    len(n_split) > len(dot_split): n_split,
    len(n_split) == len(dot_split): dot_split   
  }[True]

def run(model, ctx):
    cfg_folder = getenv("CONFIG_FOLDER")

    print('Generating music...' ,flush=True)
    
    savepath = path.join(path.abspath(cfg_folder), 'img2vid', 'out.wav')

    pipe = pipeline("text-to-audio", model)
    response = pipe(ctx, max_new_tokens=50)

    scipy.io.wavfile.write(savepath, rate=response["sampling_rate"], data=response["audio"])

    return savepath
