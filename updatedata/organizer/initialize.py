from ..database.blankdb import blank_db
from util import assetmanager

import os.path
import shutil


# Prepares tmp folder structure and databases and copies the live/stashed ones over
def initialize(overseer):
    assetmanager.check_folder_structure()

    tmp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".tmp"))
    if os.path.isdir(tmp_path):
        shutil.rmtree(tmp_path)

    os.mkdir(tmp_path)
    os.mkdir(os.path.join(tmp_path, "images"))
    os.mkdir(os.path.join(tmp_path, "images", "items"))
    os.mkdir(os.path.join(tmp_path, "images", "abilities"))
    os.mkdir(os.path.join(tmp_path, "images", "heroes"))

    db_path = os.path.join(tmp_path, "db")
    os.mkdir(db_path)
    for language in overseer.languages:
        language_path = os.path.join(db_path, language)
        os.mkdir(language_path)
        new_path = os.path.join(language_path, "new.db")
        blank_db(new_path)

        src = assetmanager.find_db(language)
        dst = os.path.join(language_path, "old.db")
        if not src:
            blank_db(dst)
        else:
            shutil.copyfile(src, dst)
