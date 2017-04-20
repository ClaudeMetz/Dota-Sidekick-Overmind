import os
import shutil

from .overseer import asset_path, base_path


# Manages the asset folder


# Checks and corrects the basic folder structure within the asset folder
def prepare_folder_structure():
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
    dst = os.path.join(asset_path, folder, "db", language + ".db")
    shutil.copyfile(src, dst)
