import os.path
import shutil


# Cleans up tmp folder if necessary
def cleanup(overseer):
    if overseer.dev_settings["tmp_conservation"] == 0:
        tmp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".tmp"))
        if os.path.isdir(tmp_path):
            shutil.rmtree(tmp_path)
