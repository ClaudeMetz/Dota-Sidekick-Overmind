import json
import os.path


# Handles settings and general data for all parts of the project
# Data: patch_history
# Settings: dev_settings, caching, languages
class Overseer:
    # Loads all settings and data and saves it as instance variables
    def __init__(self):
        self.tmp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "updatedata", ".tmp"))
        self.storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))

        with open(os.path.join(self.storage_path, "data.json"), mode="r") as data_file:
            data = json.loads(data_file.read())
        self.patch_history = data["patch_history"]
        self.lang_shorthand = data["lang_shorthand"]

        with open(os.path.join(self.storage_path, "settings.json"), mode="r") as settings_file:
            settings = json.loads(settings_file.read())
        self.dev_settings = settings["dev_settings"]
        self.caching = settings["caching"]
        self.languages = settings["languages"]

        self.dev_settings_enabled = False
        for setting in self.dev_settings.values():
            if setting == 1:
                self.dev_settings_enabled = True
                break

        self.caching_enabled = False
        for setting in self.caching.values():
            if setting == 1:
                self.caching_enabled = True
                break

    # For convenient use of 'with'
    def __enter__(self):
        return self

    # Writes all data to disk as it could have changed during runtime
    def __exit__(self, exc_type, exc_val, exc_tb):
        data = {"patch_history": self.patch_history, "lang_shorthand": self.lang_shorthand}
        with open(os.path.join(self.storage_path, "data.json"), mode="w") as data_file:
            data_file.write(json.dumps(data, indent=4))

    # Returns the status of the current dev-related settings:
    def dev_mode(self):
        status = []
        if self.dev_settings_enabled:
            status.append("dev settings enabled")
        else:
            status.append("dev settings disabled")
        status.append(" | ")
        if self.caching_enabled:
            status.append("caching enabled")
        else:
            status.append("caching disabled")
        return "".join(status)

    # Returns the last patch that was added
    def last_patch(self):
        return self.patch_history[-1]
