def run(model, ctx):
    print('\nGenerating online output for question: ' + ctx, flush=True)

    import g4f
    g4f.debug.logging = True
    response = g4f.ChatCompletion.create(
        model=model["model"],
        messages=[{"role": "user", "content": ctx}]
    )

    return response