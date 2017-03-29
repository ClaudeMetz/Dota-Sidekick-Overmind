from util.overseer import Overseer
from updatedata.organizer.initialize import initialize
from updatedata.organizer.cleanup import cleanup
from updatedata.organizer.cacher import Cacher
from updatedata.crawler.items import crawl_items

import traceback


# Updates the production database for a new patch
def update_data():
    with Overseer() as overseer:
        try:
            print(overseer.dev_mode())
            print("Last recorded patch: " + overseer.last_patch())

            correct = "n"
            while correct != "y":
                patch = input("Enter the version number of the new patch: ")
                correct = input("Is '" + patch + "' correct? (y/n): ")
            print("Updating database...")

            initialize(overseer)
            print("Setup complete!")

            cacher = Cacher(overseer)
            crawl_items(cacher)
            print("Crawling complete!")

            cleanup(overseer)
            print("Database successfully updated!")
        except Exception:
            print(traceback.print_exc())
            cleanup(overseer)


if __name__ == '__main__':
    update_data()
