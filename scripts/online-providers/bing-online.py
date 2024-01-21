import g4f, sys
from g4f.Provider.bing.create_images import patch_provider

if len(sys.argv) != 2:
    print("Prompt missing!")
    sys.exit(1)

ctx = sys.argv[1]

response=g4f.ChatCompletion.create(
    model=g4f.models.default,
    provider=g4f.Provider.Bing,
    messages=[{"role": "user", "content": "GENERATE IMAGE: " + ctx}],
    cookies=
    patch_provider=patch_provider
)

print(response)

# Extract text inside quotes
inside_quotes = False
result = []
for char in response:
    if char == '"':
        inside_quotes = not inside_quotes
        if not inside_quotes:
            break  # Break out of the loop after the first closing quote
    elif inside_quotes:
        result.append(char)

result = ''.join(result)

print('Writing to file: ' + result)

with open('./prompt.txt', 'w') as file:
    file.write(result)

print('Generated prompt.txt')
