from os import getenv
from subprocess import run

FAST_MODE = getenv('FAST_MODE')
IS_IMAGE = getenv('IS_IMAGE')
PROMPT = getenv('PROMPT')
ENH_PROMPT = getenv('ENH_PROMPT')

def from_imput():
    print("Using direct prompt from input.")
    run(f'echo "{PROMPT}" > prompt-0.txt')

def from_imput_enhance(fastMode):
    if(fastMode):
        print("Using prompt from input, enhancing fastly...")
        run(f'echo online=true >> $GITHUB_OUTPUT', shell=True)
    else: 
       print("Using prompt from input, enhancing via local language model...")
    run(f'echo enhance=true >> $GITHUB_OUTPUT', shell=True)

def autonomous(fastMode):
    if(fastMode):
        print("Using autonomous prompt, generating fastly...")
        run(f'echo online=true >> $GITHUB_OUTPUT', shell=True)
    else: 
        print("Using autonomous prompt, generating via local language model...")
    run(f'echo auto=true >> $GITHUB_OUTPUT', shell=True)

if IS_IMAGE.strip() == 'true':
    print("Using image as input.")

else:
    if bool(PROMPT.strip()):
        if ENH_PROMPT.lower() == "true":
            from_imput_enhance(True if FAST_MODE.lower() == "true" else False)
        else:
            from_imput()
    else:
        autonomous(True if FAST_MODE.lower() == "true" else False)