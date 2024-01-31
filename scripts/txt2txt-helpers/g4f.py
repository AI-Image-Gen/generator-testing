
def run(model, ctx):

    import g4f
    print('\nGenerating online output for question: ' + ctx, flush=True)

    g4f.debug.logging = True
    response = g4f.ChatCompletion.create(
        model=model["model"],
        messages=[{"role": "user", "content": ctx}]
    )

    return response