import g4f

def run(model, ctx):    
    print('\nGenerating online output for question: ' + ctx, flush=True)

    g4f.debug.logging = True
    response = g4f.ChatCompletion.create(
        model=model["model"],
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
    
    print('\n\nResponse: ' + response, flush=True)
    print("\n\nFormatted to: " + result, flush=True)

    return response