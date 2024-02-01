from transformers import GPT2Tokenizer, GPT2Model

def run(model, ctx):    
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = GPT2Tokenizer.from_pretrained(model["model"])
    model = GPT2Model.from_pretrained(model["model"])

    inputs = tokenizer(ctx, return_tensors="pt")

    output = model(**inputs)
    response = tokenizer.decode(output["output_ids"][0], skip_special_tokens=True)

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