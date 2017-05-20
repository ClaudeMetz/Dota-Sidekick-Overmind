from .detect_change import detect_change
from ..crawler.heroes import HeroCrawler
from ..crawler.items import ItemCrawler
from ..crawler.overviews import list_items, list_heroes
from ..database.session_scope import session_scope
from ..etc.cacher import Cacher


# Populates the databases for all languages
def populate(overseer, patch, revision):
    verbose = overseer.dev_settings["verbose_console"]
    eng_cacher = Cacher(overseer, "english")
    item_list = list_items(eng_cacher)
    hero_list = list_heroes(eng_cacher)

    for language in overseer.languages:
        print("Populating for {} ...".format(language))
        if language == "english":  # So the www-cacher doesn't initialize twice
            cacher = eng_cacher
        else:
            cacher = Cacher(overseer, language)

        with session_scope(language) as session:
            if overseer.dev_settings["no_item_populating"] != 1:
                item_generator = ItemCrawler(cacher, patch, revision).crawl(item_list)
                for item in item_generator:
                    if verbose == 1:
                        print(item.dname)

                    if detect_change(session, item):
                        session.add(item)
                print("Items complete!")

            if overseer.dev_settings["no_hero_populating"] != 1:
                hero_generator = HeroCrawler(cacher, patch, revision).crawl(hero_list)
                for hero in hero_generator:
                    if verbose == 1:
                        print(hero.dname)

                    # The following is a bit convoluted, but serves the purpose of working around some SQLAlchemy
                    #  'limitations' in how inserting works, specifically how when you insert 'hero', it inserts all
                    #  appendages, and doesn't insert them if 'hero' itself hasn't changed
                    appendages = hero.abilities + hero.talents
                    for appendage in appendages:
                        if not detect_change(session, appendage):
                            appendage_class = type(appendage).__name__
                            if appendage_class == "Ability":
                                hero.abilities.remove(appendage)
                            elif appendage_class == "Talent":
                                hero.talents.remove(appendage)

                    if detect_change(session, hero):
                        session.add(hero)
                    elif hero.abilities or hero.talents:
                        appendages = hero.abilities + hero.talents
                        for appendage in appendages:
                            session.add(appendage)
                print("Heroes complete!")
