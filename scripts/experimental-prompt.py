import json, sys, os
from transformers import AutoModelForCausalLM, AutoTokenizer

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Json config file path missing!")
    sys.exit(1)
    
with open(sys.argv[1] + '/langModel.json', 'r') as file:
    data = json.load(file)

with open(sys.argv[1] + '/usedPrompts.json', 'r') as file:
    usedPrompts = json.load(file)

all_justusedprompts = []
justusedprompts = os.listdir('.')
justusedprompts_list = [file for file in justusedprompts if file.endswith(".txt")]
for txt_file in justusedprompts_list:
    file_path = os.path.join('.', txt_file)  # Construct the full file path
    with open(file_path, 'r') as file:
        prompt = file.read()
        all_justusedprompts.append(prompt)

ctx = data["prompt"] + " It must be EXACTLY AND ONLY 1 PROMPT, FORMATTED LIKE THAT: \"PROMPT\". You can't use these prompts: " + '\n' + '\n'.join(usedPrompts) + '\n' + '\n'.join(all_justusedprompts)

# Enhance non-auto prompt
if len(sys.argv) == 3:
    ctx = "Give me 1 nice prompt for ai image generator, that needs to generate \"" + sys.argv[2] + "\". It must be EXACTLY AND ONLY 1 PROMPT, FORMATTED LIKE THAT: \"PROMPT\". You can't use these prompts:" + '\n' + '\n'.join(all_justusedprompts)

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

# Extract text inside quotes from assistant response
start_index = response.find('<|assistant|>')
response = response[start_index + len('<|assistant|>'):]
inside_quotes = False
result = []
for char in response:
    if char == '"':
        inside_quotes = not inside_quotes
        if not inside_quotes:
            break  # Break out of the loop after the first closing quote
    elif inside_quotes:
        result.append(char)

result = ''.join(result)

print('Result:' + result)
print('Response: ' + response)

print('Writing to file: ' + result)

with open('./prompt.txt', 'w') as file:
    file.write(result)

print('Generated prompt.txt')
