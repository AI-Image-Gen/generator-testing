from subprocess import run
import os, shutil, json

config_dir = os.getenv('CONFIG_FOLDER')

with open(os.path.join(config_dir, 'tmp', 'settings', 'cfg.json'), 'r') as file:
    config = json.load(file)
    
if config["global"]["clean_artifacts"]:
    def organize_and_rename(root_folder):
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                old_path = os.path.join(root, file)
                
                # Extract the common prefix (e.g., img2img or img2vid)
                common_prefix = os.path.basename(root).split('-')[0].strip()

                # Extract the suffix (e.g., sth-1, sth-2) from the folder name
                folder_suffix = os.path.basename(root).replace(common_prefix + '-', '').strip()

                # Construct the new filename
                new_name = os.path.splitext(file)[0] + '_' + folder_suffix + os.path.splitext(file)[1]
                new_folder_path = os.path.abspath(os.path.join(root_folder, common_prefix))
                new_path = os.path.join(new_folder_path, new_name)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                    print(f'Created common folder: {new_folder_path}')

                # Rename the file
                shutil.move(old_path, new_path)
                print(f'Moved: {old_path} -> {new_path}')

    dirs_to_del = ['prompt', 'settings']
    for todel in dirs_to_del:
        todel_dir = os.path.join(config_dir, 'tmp', todel)
        if os.path.exists(todel_dir):
            shutil.rmtree(os.path.join(config_dir, 'tmp', todel))

    organize_and_rename(os.path.join(config_dir, 'tmp'))

    path = os.path.join(os.path.abspath(config_dir), 'tmp', 'txt2img')
    run(f'echo txt2img={path} >> $GITHUB_OUTPUT', shell=True)

    path = os.path.join(os.path.abspath(config_dir), 'tmp', 'img2img')
    run(f'echo img2img={path} >> $GITHUB_OUTPUT', shell=True)

    path = os.path.join(os.path.abspath(config_dir), 'tmp', 'img2vid')
    run(f'echo img2vid={path} >> $GITHUB_OUTPUT', shell=True)

    path = os.path.join(os.path.abspath(config_dir), 'tmp', 'upscale')
    run(f'echo upscale={path} >> $GITHUB_OUTPUT', shell=True)

    run(f'echo cleanup=true >> $GITHUB_OUTPUT', shell=True)

else:
    run(f'echo cleanup=false >> $GITHUB_OUTPUT', shell=True)


if config["txt2txt"]["save_as_used"] and config["txt2txt"]["active"]:
    print('Saving txt2txt prompts as used...')

    txt2txt = json.loads(os.getenv("txt2txt").replace('*', ' '))

    with open(os.path.join(config_dir, 'usedPrompts.json'), 'r') as file:
        data = json.load(file)
    for prompt in txt2txt:
        data.append(prompt)
    while len(data) > 10:
        data.pop(0)
    with open(os.path.join(config_dir, 'usedPrompts.json'), 'w') as file:
        json.dump(data, file, indent=2)

    command = """
    git config --global user.name ai &&
    git config --global user.email github-actions@github.com &&
    git add . &&
    git commit -m 'Add used prompts'
    """

    run(command, shell=True, check=True, cwd='../')
    run('echo push=true >> $GITHUB_OUTPUT', shell=True)

else: 
    run('echo push=false >> $GITHUB_OUTPUT', shell=True)