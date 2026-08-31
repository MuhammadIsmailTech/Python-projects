import os
import shutil

def create_folder(name):
    if not os.path.exists(name):
        os.mkdir(name)
        print("Folder created:", name)
    else:
        print("Folder already exists")

def create_file(name):
    with open(name, "w") as f:
        f.write("Automation bot created this file.")
    print("File created:", name)

def rename_item(old, new):
    os.rename(old, new)
    print("Renamed:", old, "→", new)

def delete_item(name):
    if os.path.isfile(name):
        os.remove(name)
        print(f"File '{name}' deleted.")
    elif os.path.isdir(name):
        shutil.rmtree(name)
        print(f"Folder '{name}' deleted.")
    else:
        print(f"'{name}' does not exist.")
