from transformers import AutoModelForCausalLM, AutoTokenizer

def run(model, ctx):  
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = AutoTokenizer.from_pretrained(model["model"])
    model = AutoModelForCausalLM.from_pretrained(model["model"])

    inputs = tokenizer(ctx, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=2048)
    response = tokenizer.decode(outputs[0])

    result = response.split("Output: ")[1].strip()

    print('\n\nResponse: ' + response, flush=True)
    print("\n\nFormatted to: " + result, flush=True)

    return response