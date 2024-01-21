from os import path, getenv, listdir
from subprocess import run
from json import load
from sys import argv

AUTO = getenv('AUTO')
PROMPT = getenv('PROMPT')
AMOUNT = getenv('AMOUNT')
REPO_DIR = getenv('REPO_DIR')
CONFIG_FOLDER = getenv('CONFIG_FOLDER')
ONLINE_MODE = True if len(argv) > 1 and argv[1] == 'ONLINE' else False

with open(path.join(REPO_DIR, CONFIG_FOLDER, 'models.json'), 'r') as file:
    if ONLINE_MODE:
        data = load(file)["lang-online"]
    else:
        data = load(file)["lang-offline"]

with open(path.join(REPO_DIR, CONFIG_FOLDER, 'usedPrompts.json'), 'r') as file:
    usedPrompts = load(file)

for num in AMOUNT:
    all_justusedprompts = []
    justusedprompts = listdir(path.join(REPO_DIR, CONFIG_FOLDER))
    justusedprompts_array = [file for file in justusedprompts if file.endswith(".txt")]
    for txt_file in justusedprompts_array:
        file_path = path.join(REPO_DIR, CONFIG_FOLDER, txt_file)  # Construct the full file path
        with open(file_path, 'r') as file:
            prompt = file.read()
            all_justusedprompts.append(prompt)

    if AUTO == "true":
        ctx = data["prompt_template"].format(
            prompt="",
            used_prompts=data["used_prompts_template"].format(used_prompts='\n'.join(all_justusedprompts)+'\n'.join(usedPrompts))
        )
    else:
        ctx = data["prompt_template"].format(
            prompt=PROMPT,
            used_prompts=data["used_prompts_template"].format(used_prompts='\n'.join(all_justusedprompts)) if all_justusedprompts else ""
        )

    if ONLINE_MODE:
        print('\nGenerating online output for question: ' + ctx)
        import g4f

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

    else:
        print('\nGenerating offline output for question: ' + ctx)
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-zephyr-1_6b', trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            'stabilityai/stablelm-2-zephyr-1_6b',
            trust_remote_code=True,
            device_map="auto"
        )

        prompt = [{'role': 'user', 'content': ctx}]
        inputs = tokenizer.apply_chat_template(
            prompt,
            add_generation_prompt=True,
            return_tensors='pt'
        )

        tokens = model.generate(
            inputs.to(model.device),
            max_new_tokens=1024,
            temperature=0.5,
            do_sample=True
        )
        response = tokenizer.decode(tokens[0], skip_special_tokens=False)

        start_index = response.find('<|assistant|>')
        response = response[start_index + len('<|assistant|>'):]
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


    print('\n\nOutput: ' + response)
    print("\n\nFormatted to: " + result)

    with open(path.join(REPO_DIR, CONFIG_FOLDER, f'prompt-{num}.txt'), 'w') as file:
        file.write(result)

print('Generated all prompt.txt files.')