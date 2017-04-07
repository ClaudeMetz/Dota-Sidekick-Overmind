import re


# Handles the entry procedure
def user_input(overseer):
    patch = "dev"
    revision = 0
    if overseer.dev_settings["skip_intro_questions"] == 0:
        patch = collect_input("patch name", check_patch, overseer)
        revision = collect_input("revision", check_revision, overseer)
    return patch, revision


# Collects, confirms and checks user-input
def collect_input(name, check, overseer):
    confirmed = "n"
    correct = False
    answer = ""
    while (confirmed != "y") or not correct:
        answer = input("Enter the " + name + " for the new version: ")
        confirmed = input("Is '" + answer + "' correct? (y/n): ")
        if confirmed == "y":
            correct = check(overseer, answer)
    return answer


# Sanity-check for the entered patch name
def check_patch(overseer, answer):
    version = overseer.last_version()
    if re.match("^7\.[0-9]{2}[a-z]?$", answer) and answer >= version[0]:
        return True
    else:
        print("The entered patch does not match the necessary criteria.")
        return False


# Sanity-check for the entered revision
def check_revision(overseer, answer):
    version = overseer.last_version()
    if re.match("^[0-9]+$", answer):
        return True
    else:
        print("The entered revision does not match the necessary criteria.")
        return False
