from .detect_change import detect_change
from ..crawler.heroes import HeroCrawler
from ..crawler.items import ItemCrawler
from ..crawler.overviews import list_items, list_heroes
from ..database.session_scope import session_scope
from ..etc.cacher import Cacher


# Populates the databases for all languages
def populate(overseer, patch, revision):
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
            item_generator = ItemCrawler(cacher, patch, revision).crawl(item_list)
            for item in item_generator:
                if detect_change(session, item):
                    session.add(item)
            print("Items complete!")

            hero_generator = HeroCrawler(cacher, patch, revision).crawl(hero_list)
            for hero in hero_generator:
                if detect_change(session, hero):
                    session.add(hero)
                appendages = hero.abilities + hero.talents
                for appendage in appendages:
                    if detect_change(session, appendage):
                        session.add(appendage)
            print("Heroes complete!")
