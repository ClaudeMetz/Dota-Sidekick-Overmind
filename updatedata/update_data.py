import traceback

from updatedata.database.populate import populate
from updatedata.organizer.cleanup import cleanup
from updatedata.organizer.deploy import deploy
from updatedata.organizer.initialize import initialize
from updatedata.organizer.user_input import UserInput
from util.overseer import Overseer


# Updates the production database for a new patch
def update_data():
    with Overseer() as overseer:
        try:
            print(overseer.dev_mode())
            old_version = overseer.last_version()
            if old_version:
                last_version_str = "Last recorded version: Patch '{patch}' Revision {revision}"
                print(last_version_str.format(patch=old_version[0], revision=str(old_version[1])))
            else:
                print("No prior version")

            version = UserInput(overseer).collect()
            new_version_str = "Updating database (Patch '{patch}' Revision {revision}) ..."
            print(new_version_str.format(patch=version[0], revision=str(version[1])))

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
