import sys, json

with open('./prompt.txt', 'r') as file:
    prompt = file.read()

with open(sys.argv[1] + '/usedPrompts.json', 'r') as file:
    data = json.load(file)

while len(data) >= 10:
    data.pop(0)

data.append(prompt)
with open(sys.argv[1] + '/usedPrompts.json', 'w') as file:
    json.dump(data, file, indent=2) 