import os.path
import shutil


# Prepares tmp folder structure and databases
def initialize(overseer):
    tmp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp"))
    if os.path.isdir(tmp_path):
        shutil.rmtree(tmp_path)

    os.mkdir(tmp_path)
    os.mkdir(os.path.join(tmp_path, "images"))
    os.mkdir(os.path.join(tmp_path, "images", "items"))
    os.mkdir(os.path.join(tmp_path, "images", "abilities"))
    os.mkdir(os.path.join(tmp_path, "images", "heroes"))

    os.mkdir(os.path.join(tmp_path, "db"))
    for language in overseer.languages:
        os.mkdir(os.path.join(tmp_path, "db", language))
