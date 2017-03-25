import json
import os.path

# Handles settings and general data for all parts of the project
# Data: patch_history
# Settings: dev_settings
class Overseer:
    # Loads all settings and data and saves it as instance variables
    def __init__(self):
        self.storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))

        with open(os.path.join(self.storage_path, "data.json"), mode="r") as data_file:
            data = json.loads(data_file.read())
        self.patch_history = data["patch_history"]

        with open(os.path.join(self.storage_path, "settings.json"), mode="r") as settings_file:
            settings = json.loads(settings_file.read())
        self.dev_settings = settings["dev_settings"]
        self.languages = settings["languages"]

    # For convenient use of 'with'
    def __enter__(self):
        return self

    # Writes all data to disk as it could have changed during runtime
    def __exit__(self, exc_type, exc_val, exc_tb):
        data = {"patch_history": self.patch_history}
        with open(os.path.join(self.storage_path, "data.json"), mode="w") as data_file:
            data_file.write(json.dumps(data, indent=4))

    # Checks if any dev-settings are enabled and returns a fitting status
    def dev_mode(self):
        message = "(dev-mode inactive)"
        for setting in self.dev_settings.values():
            if setting == 1:
                message = "(dev-mode active)"
                break
        return message

    # Returns the last patch that was added
    def last_patch(self):
        return self.patch_history[-1]
