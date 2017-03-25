# Verifies the data entered into the classes to prevent database insertion errors

# Checks if an ability or talent matches the hero class it is being attached to and adds it to the respective array
def check_compatibility(hero, appendage):
    if appendage.hero == hero.name:
        if type(appendage).__name__ == "Ability":
            hero.abilities.append(appendage)
        else:
            hero.talents.append(appendage)
    else:
        raise WrongHeroException(hero.name, appendage)


# Check if the object has data for all fields required by the database
def check_completeness(obj):
    complete = True
    missing_data = []
    for dataset in obj.get_required().items():
        if dataset[1] is None:
            complete = False
            missing_data.append(dataset[0])
    if not complete:
        raise MissingDataException(obj, missing_data)


# Gets raised when an ability or a talent is added to a non-matching hero class
class WrongHeroException(Exception):
    def __init__(self, hero_name, appendage):
        if type(appendage).__name__ == "Ability":
            self.message = "The ability '" + str(appendage) + "' does not match the hero '" + hero_name + "'"
        else:
            self.message = "The talent '" + str(appendage) + "' does not match the hero '" + hero_name + "'"

    def __str__(self):
        return self.message


# Gets raised when an object misses data that is required by the database
class MissingDataException(Exception):
    def __init__(self, obj, missing_data):
        self.message = "The dataset " + str(obj) + " is missing this data: " + ", ".join(missing_data)

    def __str__(self):
        return self.message
