

# Updates the production database for a new patch
def update_data():
    correct = "n"
    while correct != "y":
        patch = input("Enter the version number of the new patch: ")
        correct = input("Is " + patch + " correct? (y/n): ")
    print("Updating database...")

    print("Done!")

    # Procedure step by step:
    #   (Note: this procedure will be manually kicked off for now)
    #   Info: Ask for patch name and other relevant data
    # Setup: Setup (temporary) databases, folders through fitting handler classes/functions
    # Crawling: Crawl items, heroes and their abilities and talents
    # Manipulation: When necessary, manipulate the data further
    # Saving: Save the polished data to the database through a handler
    # Deployment: Deploy new data to production and clean up, save settings


if __name__ == '__main__':
    update_data()
