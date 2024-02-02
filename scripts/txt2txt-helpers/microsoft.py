from transformers import AutoModelForCausalLM, AutoTokenizer
import os, re

def run(model, ctx, num):
    cfg_folder = os.getenv('CONFIG_FOLDER')
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = AutoTokenizer.from_pretrained(model["model"])
    model = AutoModelForCausalLM.from_pretrained(model["model"])

    inputs = tokenizer(ctx, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=256, do_sample=False, num_return_sequences=num)
    
    for number in range(num):
        response = tokenizer.decode(outputs[number], skip_special_tokens=True)
        
        result = response.split("Output: ")[1].strip().replace('"', "'")
        result = re.sub('!.+?\)', '', result)

        with open(os.path.join(cfg_folder, 'prompts', f'prompt-{number}.txt'), 'w') as file:
            file.write(result)
            
        print('\n\nResponse: ' + response, flush=True)
        print("\n\nFormatted to: " + result, flush=True)

    return os.path.join(cfg_folder, 'prompts')
