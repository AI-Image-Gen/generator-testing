from os import getenv, path, listdir
import json
from subprocess import run

cfg_folder = getenv("CONFIG_FOLDER")

run('pip install -U g4f~=0.2.0.7', shell=True)

import g4f

with open(path.join(cfg_folder, 'usedPrompts.json'), 'r') as file:
    usedPrompts = json.load(file)

with open(path.join(cfg_folder, 'cfg.json'), 'r') as file:
        data = json.load(file)

run(f'mkdir -p {path.join(cfg_folder, "prompts")}', shell=True)
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

    
    data_str = json.dumps(data)
    # Add old prompts
    used_prompts_str = '\n'.join(f'"{prompt}"' for prompt in usedPrompts) + '\n' + '\n'.join(f'"{prompt}"' for prompt in all_justusedprompts)
    data_str = data_str.replace('{global.used_prompts}', used_prompts_str)
    data = json.loads(data_str)

    # Add current prompt
    prompt_str = data["txt2txt"]["prompt"]
    data_str = data_str.replace('{txt2txt.prompt}', prompt_str)
    data = json.loads(data_str)

    ctx = data["txt2txt"]["prompt_pre"]

    print('\nGenerating online output for question: ' + ctx)

    g4f.debug.logging = True
    response = g4f.ChatCompletion.create(
        model=data["model"],
        messages=[{"role": "user", "content": ctx}]
    )

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

    print('\n\Response: ' + response)
    print("\n\nFormatted to: " + result)

    with open(path.join(cfg_folder, 'prompts', f'prompt-{num}.txt'), 'w') as file:
        file.write(result)

# Get all prompts
prompts_arr = []
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
        prompts_json_str = '{"num":"current"'.replace("current", prompts_arr[num]).replace("num", num).replace(" ", '~')
    else:
        prompts_json_str = prompts_json_str + ',"num":"current"'.replace("current", prompts_arr[num]).replace("num", num).replace(" ", '~')
prompts_json_str = prompts_json_str + "}"

run(f'echo out={prompts_json_str} >> $GITHUB_OUTPUT', shell=True)

print(f'Generated all prompt.txt files and set out to {prompts_json_str}')