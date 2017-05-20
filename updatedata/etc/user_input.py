import re


class UserInput:
    def __init__(self, overseer):
        self.overseer = overseer
        self.patch = "dev"
        self.revision = 1
        self.verify_func = {
            "Patch": self.verify_patch,
            "Revision": self.verify_revision
        }
        self.last_version = overseer.last_version()
        if not self.last_version:
            self.last_version = ("0", 0)
            # This ensures that the entered version is always accepted if syntactically correct

    # Collects, confirms and verifies user-input
    def collect(self):
        if self.overseer.dev_settings["skip_intro_questions"] == 0:
            self.patch = self.input("Patch")
            self.revision = int(self.input("Revision"))
        return self.patch, self.revision

    # Collects, confirms and verifies user-input
    def input(self, choice):
        confirmed = "n"
        correct = False
        answer = ""
        while (confirmed != "y") or not correct:
            answer = input("Enter the {} for the new version: ".format(choice))
            confirmed = input("Is '{}' correct? (y/n): ".format(answer))
            if confirmed == "y":
                correct = self.verify_func[choice](answer)
                if not correct:
                    print("The entered {} does not match the necessary criteria.".format(choice))
        return answer

    # Sanity-check for the entered patch
    def verify_patch(self, answer):
        if re.fullmatch("7\.[0-9]{2}[a-z]?", answer) and answer >= self.last_version[0]:
            return True
        else:
            return False

    # Sanity-check for the entered revision
    def verify_revision(self, answer):
        if self.patch == self.last_version[0]:
            if re.fullmatch("[0-9]+", answer) and int(answer) > self.last_version[1]:
                return True
        else:
            if answer == "1":
                return True
        return False
