from util.overseer import Overseer
from updatedata.organizer.initialize import initialize
from updatedata.organizer.cleanup import cleanup
from updatedata.database.populate import populate

import traceback


# Updates the production database for a new patch
def update_data():
    with Overseer() as overseer:
        try:
            print(overseer.dev_mode())
            print("Last recorded patch: " + overseer.last_patch())

            patch = "dev"
            if overseer.dev_settings["skip_intro_questions"] == 0:
                correct = "n"
                while correct != "y":
                    patch = input("Enter the version number of the new patch: ")
                    correct = input("Is '" + patch + "' correct? (y/n): ")
            print("Updating database...")

            initialize(overseer)
            print("Setup complete!")

            populate(overseer, patch)
            print("Crawling complete!")

            cleanup(overseer)
            # overseer.patch_history.append(patch)
            print("Database successfully updated!")
        except Exception:
            print(traceback.print_exc())
            cleanup(overseer)


if __name__ == '__main__':
    update_data()
