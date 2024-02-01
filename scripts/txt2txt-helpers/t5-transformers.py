from transformers import T5Tokenizer, T5ForConditionalGeneration

def run(model, ctx):    
    print('\nGenerating output for question: ' + ctx, flush=True)

    tokenizer = T5Tokenizer.from_pretrained(model["model"], max_new_tokens=1024)
    model = T5ForConditionalGeneration.from_pretrained(model["model"])

    input_ids = tokenizer(ctx, return_tensors="pt").input_ids

    outputs = model.generate(input_ids)
    response = tokenizer.decode(outputs[0])

    return response