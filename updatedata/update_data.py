from util.overseer import Overseer
from updatedata.organizer.initialize import initialize
from updatedata.organizer.cleanup import cleanup
from updatedata.organizer.deploy import deploy
from updatedata.organizer.user_input import user_input
from updatedata.database.populate import populate

import traceback


# Updates the production database for a new patch
def update_data():
    with Overseer() as overseer:
        try:
            print(overseer.dev_mode())
            old_version = overseer.last_version()
            print("Last recorded version: Patch " + old_version[0] + " Revision " + str(old_version[1]))

            version = user_input(overseer)
            print("Updating database (Patch " + version[0] + " Revision " + str(version[1]) + ") ...")

            initialize(overseer)
            print("Setup complete!")

            populate(overseer, version[0], str(version[1]))
            print("Crawling & Populating complete!")

            deploy(overseer)
            print("Deployment complete!")

            overseer.add_version(version)
            cleanup(overseer)
            print("Database successfully updated!")
        except Exception:
            print(traceback.print_exc())
            cleanup(overseer)


if __name__ == '__main__':
    update_data()
