import os
import shutil

# Manages the asset folder


# Checks and corrects the basic folder structure within the asset folder
def check_folder_structure():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    folders = ([
        ["asset"],
        ["asset", "live"],
        ["asset", "live", "db"],
        ["asset", "stashed"],
        ["asset", "stashed", "db"]
    ])

    for folder in folders:
        path = os.path.join(base_path, *folder)
        if not os.path.isdir(path):
            os.mkdir(path)


# Finds the database specified by the language parameter
def find_db(language):
    asset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "asset"))
    paths = [
        ["live", "db"],
        ["stashed", "db"]
    ]

    for path in paths:
        path.append(language + ".db")
        full_path = os.path.join(asset_path, *path)
        if os.path.isfile(full_path):
            return full_path


# Deploys the database from the given path to the specified asset folder
def deploy_db(src, overseer):
    language = src.split(os.sep)[-2]
    if overseer.languages[language] == 1:
        folder = "live"
    else:
        folder = "stashed"
    dst = os.path.join(overseer.asset_path, folder, "db", language + ".db")
    shutil.copyfile(src, dst)
