import sys, json, subprocess

if len(sys.argv) != 2:
    print("Multiplier amount not found!")
    sys.exit(1)

json_array = [i for i in range(int(sys.argv[1]))]
json_variable = json.dumps(json_array).replace(" ", "")

subprocess.run(f'echo amount="{json_variable}" >> $GITHUB_OUTPUT', shell=True)