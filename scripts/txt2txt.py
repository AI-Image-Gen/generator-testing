from os import getenv, path, listdir, makedirs
import json
from subprocess import run
import importlib

cfg_folder = getenv("CONFIG_FOLDER")

with open(path.join(cfg_folder, 'usedPrompts.json'), 'r') as file:
    usedPrompts = json.load(file)

with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
    data = json.load(file)

with open(path.join(cfg_folder, 'models.json'), 'r') as file:
    models = json.load(file)["txt2txt"] 

makedirs(path.join(cfg_folder, "prompts"), exist_ok=True)

run(f"pip install {' '.join(models['gpt-4']['packages'])}", shell=True)
for num in range(int(data["global"]["out_amount"])):
    # Restore variables on every literation
    with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
        data = json.load(file)

    all_justusedprompts = []
    justusedprompts = listdir(path.join(cfg_folder, 'prompts'))
    justusedprompts_array = [file for file in justusedprompts if file.endswith(".txt")]
    for txt_file in justusedprompts_array:
        file_path = path.join(cfg_folder, 'prompts', txt_file)  # Construct the full file path
        with open(file_path, 'r') as file:
            prompt = file.read()
            all_justusedprompts.append(prompt)

    
    models_str = json.dumps(models)
    # Add old prompts
    used_prompts_str = '\\\\n'.join(p for p in usedPrompts) + '\\\\n' + '\\\\n'.join(p for p in all_justusedprompts)
    models_str = models_str.replace('{used_prompts}', used_prompts_str)
    models = json.loads(models_str)

    models_str = models_str.replace('{used_prompts_template}', models["gpt-4"]["used_prompts_template"])
    models = json.loads(models_str)

    # Add current prompt
    prompt_str = data["txt2txt"]["prompt"]
    models_str = models_str.replace('{prompt}', prompt_str)
    models = json.loads(models_str)

    ctx = models["gpt-4"]["prompt_template"]

    print('\nUsing helper: ' + models['gpt-4']['helper'], flush=True)

    helper = importlib.import_module(f"txt2txt-helpers.{models['gpt-4']['helper']}")
    response = helper.run(models["gpt-4"], ctx)

    inside_quotes = False
    result = []
    for char in response:
        if char == '"':
            inside_quotes = not inside_quotes
            if not inside_quotes:
                break
        elif inside_quotes:
            result.append(char)

    result = ''.join(result)

    print('\n\nResponse: ' + response)
    print("\n\nFormatted to: " + result)

    with open(path.join(cfg_folder, 'prompts', f'prompt-{num}.txt'), 'w') as file:
        file.write(result)

# Get all prompts
prompts_arr = []
justusedprompts = listdir(path.join(cfg_folder, 'prompts'))
prompts = [file for file in justusedprompts if file.endswith(".txt")]
for txt_file in prompts:
    file_path = path.join(cfg_folder, 'prompts', txt_file)  # Construct the full file path
    with open(file_path, 'r') as file:
        prompt = file.read()
        prompts_arr.append(prompt)

# Construct nice output
prompts_json_str = ""
for num in range(int(data["global"]["out_amount"])):
    if num == 0:
        prompts_json_str = '{"num":"current"'.replace("current", str(prompts_arr[num])).replace("num", str(num)).replace(" ", '*').replace("/n", '*')
    else:
        prompts_json_str = prompts_json_str + ',"num":"current"'.replace("current", str(prompts_arr[num])).replace("num", str(num)).replace(" ", '*').replace("/n", '*')
prompts_json_str = prompts_json_str + "}"

run(f'echo out={prompts_json_str.replace("\"", "{{\"\"}}")} >> $GITHUB_OUTPUT', shell=True)

print(f'Generated all prompt.txt files and set out to {prompts_json_str.replace("\"", "{{\"\"}}")}')