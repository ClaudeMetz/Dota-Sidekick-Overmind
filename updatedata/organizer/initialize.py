from util import assetmanager
from ..database.session_scope import session_scope

import os.path
import shutil


# Prepares tmp folder structure and databases and copies the live/stashed ones over
def initialize(overseer):
    assetmanager.check_folder_structure()

    tmp_path = overseer.tmp_path
    if os.path.isdir(tmp_path):
        shutil.rmtree(tmp_path)

    os.mkdir(tmp_path)

    db_path = os.path.join(tmp_path, "db")
    os.mkdir(db_path)
    for language in overseer.languages:
        language_path = os.path.join(db_path, language)
        os.mkdir(language_path)

        src = assetmanager.find_db(language)
        dst = os.path.join(language_path, "tmp.db")
        if src:
            shutil.copyfile(src, dst)
