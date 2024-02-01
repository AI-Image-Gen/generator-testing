from transformers import AutoModelForCausalLM, AutoTokenizer

def run(model, ctx):    
    ctx = ctx.replace(":", " -")
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = AutoTokenizer.from_pretrained(model["model"])
    model = AutoModelForCausalLM.from_pretrained(model["model"])

    inputs = tokenizer(ctx, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=4096)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print('\n\nResponse: ' + response, flush=True)

    return response