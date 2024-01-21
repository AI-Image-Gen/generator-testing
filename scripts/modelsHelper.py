import sys, json, subprocess

if len(sys.argv) != 2:
    print("Config path not found!")
    sys.exit(1)

with open(sys.argv[1] + '/models.json', 'r') as file:
    data = json.load(file)

names = [name for name in data.keys()]
if "upscaler" in names:
    names.remove("upscaler")

json_variable = json.dumps(names).replace(" ", "")

subprocess.run(f'echo models="{json_variable}" >> $GITHUB_OUTPUT', shell=True)