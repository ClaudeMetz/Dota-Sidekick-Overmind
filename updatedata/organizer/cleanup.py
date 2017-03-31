import os.path
import shutil


# Cleans up tmp folder if necessary
def cleanup(overseer):
    if overseer.dev_settings["conserve_tmp"] == 0:
        tmp_path = overseer.tmp_path
        if os.path.isdir(tmp_path):
            shutil.rmtree(tmp_path)
