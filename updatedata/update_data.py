from util.overseer import Overseer
from updatedata.organizer.initialize import initialize
from updatedata.organizer.cleanup import cleanup
from updatedata.organizer.deploy import deploy
from updatedata.database.populate import populate

import traceback
import re


# Updates the production database for a new patch
def update_data():
    with Overseer() as overseer:
        try:
            print(overseer.dev_mode())
            print("Last recorded patch: " + overseer.last_patch())

            patch = "dev"
            revision = 0
            if overseer.dev_settings["skip_intro_questions"] == 0:
                correct = "n"
                while correct != "y":
                    patch = input("Enter the version number of the new patch: ")
                    correct = input("Is '" + patch + "' correct? (y/n): ")

                rev = input("Enter the revision number for this patch (Enter = 0): ")
                if re.match("[0-9]+", rev):
                    revision = int(rev)
            print("Updating database (Patch: " + patch + " | Revision: " + str(revision) + ") ...")

            initialize(overseer)
            print("Setup complete!")

            populate(overseer, patch, revision)
            print("Crawling complete!")

            deploy(overseer)
            print("Deployment complete!")

            if overseer.dev_settings["no_patch_appending"] == 0:
                overseer.patch_history.append(patch)
            cleanup(overseer)
            print("Database successfully updated!")
        except Exception:
            print(traceback.print_exc())
            cleanup(overseer)


if __name__ == '__main__':
    update_data()
