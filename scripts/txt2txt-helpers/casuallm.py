from transformers import AutoModelForCausalLM, AutoTokenizer

def run(model, ctx):    
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = AutoTokenizer.from_pretrained(model["model"])
    model = AutoModelForCausalLM.from_pretrained(model["model"])

    inputs = tokenizer(ctx, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=2048)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

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

    if not result.strip():
        result = response

    print('\n\nResponse: ' + response, flush=True)
    print("\n\nFormatted to: " + result, flush=True)

    return response