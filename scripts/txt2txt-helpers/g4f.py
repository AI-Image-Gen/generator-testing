def run(model, ctx):
    import g4f
    g4f.debug.logging = True
    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": ctx}]
    )

    return response