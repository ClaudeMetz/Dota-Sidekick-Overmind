import json
import os.path
from collections import OrderedDict


# Handles settings and general data for all parts of the project
class Overseer:
    # Loads all settings and data and saves it as instance variables
    def __init__(self):
        this_path = os.path.abspath(os.path.dirname(__file__))
        self.asset_path = os.path.join(this_path, "..", "asset")
        self.tmp_path = os.path.join(this_path, "..", "updatedata", ".tmp")
        self.storage_path = os.path.join(this_path, "storage")

        with open(os.path.join(self.storage_path, "data.json"), mode="r") as data_file:
            data = json.loads(data_file.read())
        self.version_history = OrderedDict(data["version_history"])
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
        data = {"version_history": self.version_history, "lang_shorthand": self.lang_shorthand}
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

    # Returns the last version tuple that was added
    def last_version(self):
        patch = next(reversed(self.version_history))
        revision = self.version_history[patch][-1]
        return patch, revision

    # Adds the given version tuple to the version history
    def add_version(self, version):
        if self.dev_settings["no_patch_appending"] == 0:
            if version[0] in self.version_history:
                self.version_history[version[0]].append(version[1])
            else:
                self.version_history[version[0]] = [version[1]]
