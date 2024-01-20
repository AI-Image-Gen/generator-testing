import g4f, json, sys

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Json config file path missing!")
    sys.exit(1)
    
with open(sys.argv[1] + '/langModel.json', 'r') as file:
    data = json.load(file)

with open(sys.argv[1] + '/usedPrompts.json', 'r') as file:
    usedPrompts = json.load(file)

ctx = data["prompt"] + "It must be EXACTLY AND ONLY 1 PROMPT, FORMATTED TO BE BETWEEN \" MARKS. You can't use these prompts, find something new and interesting, not really connected with these subjects: " + '\n' + '\n'.join(usedPrompts)

# Enhance non-auto prompt
if len(sys.argv) == 3:
    ctx = "Give me 1 nice prompt for ai image generator, that needs to generate \"" + sys.argv[2] + "\". It must be EXACTLY AND ONLY 1 PROMPT, FORMATTED TO BE BETWEEN \" MARKS."

print('Generating output for question: ' + ctx)

g4f.debug.logging = True
response = g4f.ChatCompletion.create(
    model=data["model"],
    messages=[{"role": "user", "content": ctx}]
)

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