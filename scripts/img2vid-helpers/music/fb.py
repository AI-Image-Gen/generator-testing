from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from os import getenv, path

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
    model = MusicGen.get_pretrained(model)
    
    model.set_generation_params(duration=2)

    wav = model.generate(ctx)            
    for i, one_wav in enumerate(wav):
      audio_write(savepath, one_wav.cpu(), model.sample_rate, strategy="loudness")

    return savepath
