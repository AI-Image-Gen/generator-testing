from transformers import T5Tokenizer, T5ForConditionalGeneration

def run(model, ctx):    
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = T5Tokenizer.from_pretrained(model["model"])
    model = T5ForConditionalGeneration.from_pretrained(model["model"])

    input_ids = tokenizer(ctx, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_new_tokens=4096)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print('\n\nResponse: ' + response, flush=True)
    print("\n\nFormatted to: " + result, flush=True)

    return result