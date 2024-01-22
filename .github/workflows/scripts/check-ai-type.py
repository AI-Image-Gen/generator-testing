from os import getenv
from subprocess import run

FAST_MODE = getenv('FAST_MODE')
IS_IMAGE = getenv('IS_IMAGE')
PROMPT = getenv('PROMPT')
UPSCALE = getenv('UPSCALE')



else:
    if bool(PROMPT.strip()):
        if ENH_PROMPT.lower() == "true":
            from_imput_enhance(True if FAST_MODE.lower() == "true" else False)
        else:
            from_imput()
    else:
        autonomous(True if FAST_MODE.lower() == "true" else False)


if UPSCALE.strip() != 'off':
    print("Post-upscaler toggled on.")
    run(f'echo upscale=true >> $GITHUB_OUTPUT', shell=True)