import os.path
import shutil


# Cleans up tmp folder
def cleanup():
    tmp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp"))
    if os.path.isdir(tmp_path):
        shutil.rmtree(tmp_path)
