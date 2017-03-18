from util.overseer import Overseer
from updatedata.organizer.initialize import initialize
from updatedata.organizer.cleanup import cleanup


# Updates the production database for a new patch
def update_data():
    with Overseer() as overseer:
        try:
            print(overseer.dev_mode())
            print("Last recorded patch: " + overseer.patch_history)

            correct = "n"
            while correct != "y":
                patch = input("Enter the version number of the new patch: ")
                correct = input("Is '" + patch + "' correct? (y/n): ")
            print("Updating database...")

            initialize(overseer)
            print("Setup complete!")

            if overseer.dev_settings["tmp_conservation"] == 0:
                cleanup()
            print("Database successfully updated!")

            # Procedure step by step:
            #   (Note: this procedure will be manually kicked off for now)
            #   Info: Ask for patch name and other relevant data
            # Setup: Setup (temporary) databases, folders through fitting handler classes/functions
            # Crawling: Crawl items, heroes and their abilities and talents
            # Manipulation: When necessary, manipulate the data further
            # Saving & Deployment: Save the polished data to the database and deploy to production
            # Clean up: Remove tmp structures etc
        except Exception as e:
            print(e)
            if overseer.dev_settings["tmp_conservation"] == 0:
                cleanup()


if __name__ == '__main__':
    update_data()
