from transformers import AutoModelForCausalLM, AutoTokenizer
import re

def run(model, ctx):
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = AutoTokenizer.from_pretrained(model["model"])
    model = AutoModelForCausalLM.from_pretrained(model["model"])

    inputs = tokenizer(ctx, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=2048, do_sample=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    result = response.split("Output: ")[1].strip().replace('"', "'")
    result = re.sub('!.+?\)', '', result)

    print('\n\nResponse: ' + response, flush=True)
    print("\n\nFormatted to: " + result, flush=True)

    return result
