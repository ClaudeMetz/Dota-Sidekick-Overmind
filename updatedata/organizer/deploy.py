from util import assetmanager

import os


# Handles the deployment of the newly generated databases to the asset-folder
def deploy(overseer):
    if overseer.dev_settings["no_deployment"] == 0:
        dbs_path = os.path.join(overseer.tmp_path, "db")
        for directory in os.listdir(dbs_path):
            db_path = os.path.join(dbs_path, directory, "old.db")
            assetmanager.deploy_db(db_path, overseer)
