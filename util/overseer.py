import json
import os.path
from collections import OrderedDict


this_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(this_path, "..")
asset_path = os.path.join(this_path, "..", "asset")
tmp_path = os.path.join(this_path, "..", "updatedata", ".tmp")
cache_path = os.path.join(this_path, "..", "updatedata", ".cache")

storage_path = os.path.join(this_path, "storage")


# Handles settings and general data for all parts of the project
class Overseer:
    # Loads all settings and data and saves it as instance variables
    def __init__(self):
        attributes = {}

        data_dict = read_json("data.json")
        attributes.update(data_dict)
        self.data_items = list(data_dict)  # For reconstruction later

        settings_dict = read_json("settings.json")
        if settings_dict["live"] == 1:
            del settings_dict["dev_settings"]
            settings_dict["dev_settings"] = settings_dict.pop("live_settings")
        else:
            del settings_dict["live_settings"]
        attributes.update(settings_dict)

        self.__dict__.update(attributes)
        # The preceding lines automatically set all settings and data variables as class attributes for easy access

        self.dev_settings_enabled = enabled(self.dev_settings.values())
        self.caching_enabled = enabled(self.caching.values())

    # For convenient use of 'with'
    def __enter__(self):
        return self

    # Writes all data to disk as it could have changed during runtime
    def __exit__(self, exc_type, exc_val, exc_tb):
        data = {}
        for dataset in self.data_items:
            data.update({dataset: getattr(self, dataset)})
            # Reconstructs the data dictionary

        with open(os.path.join(storage_path, "data.json"), mode="w") as data_file:
            data_file.write(json.dumps(data, indent=4))

    # Returns the status of the current dev-related settings:
    def dev_mode(self):
        status = "Dev Settings {dev_settings}abled | Caching {caching}abled"

        if self.dev_settings_enabled:
            dev_settings = "en"
        else:
            dev_settings = "dis"

        if self.caching_enabled:
            caching = "en"
        else:
            caching = "dis"

        return status.format(dev_settings=dev_settings, caching=caching)

    # Returns the last version tuple that was added
    def last_version(self):
        if self.version_history:
            patch = next(reversed(self.version_history))
            revision = self.version_history[patch][-1]
            return patch, revision
        else:
            return None

    # Adds the given version tuple to the version history
    def add_version(self, version):
        if self.dev_settings["no_patch_appending"] == 0:
            if version[0] in self.version_history:
                self.version_history[version[0]].append(int(version[1]))
            else:
                self.version_history[version[0]] = [version[1]]


# Reads and returns the json specified by the given filename
def read_json(file):
    with open(os.path.join(storage_path, file), mode="r") as data_file:
        r = dict(json.loads(data_file.read(), object_pairs_hook=OrderedDict))
    return r


# Returns True when one of the items in the list are true
def enabled(values):
    en = False
    for setting in values:
        if setting == 1:
            en = True
            break
    return en
