import os.path
import shutil

from util import assetmanager
from util.overseer import tmp_path


# Prepares tmp folder structure and databases and copies the live/stashed ones over
def initialize(overseer):
    assetmanager.prepare_folder_structure()

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


# Handles the deployment of the newly generated databases to the asset-folder
def deploy(overseer):
    if overseer.dev_settings["no_deployment"] == 0:
        dbs_path = os.path.join(tmp_path, "db")
        for directory in os.listdir(dbs_path):
            db_path = os.path.join(dbs_path, directory, "tmp.db")
            assetmanager.deploy_db(db_path, overseer)


# Cleans up tmp folder if necessary
def cleanup(overseer):
    if overseer.dev_settings["conserve_tmp"] == 0:
        if os.path.isdir(tmp_path):
            shutil.rmtree(tmp_path)
