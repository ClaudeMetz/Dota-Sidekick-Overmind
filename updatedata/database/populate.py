from .detect_change import detect_change
from ..organizer.cacher import Cacher
from ..crawler.items import ItemCrawler
from ..crawler.heroes import HeroCrawler
from ..crawler.overviews import list_items, list_heroes
from ..database.session_scope import session_scope


# Populates the databases for all languages
def populate(overseer, patch, revision):
    cacher = Cacher(overseer, "english")
    item_list = list_items(cacher)
    hero_list = list_heroes(cacher)

    for language in overseer.languages:
        if language != "english":  # So the www-cacher doesn't initialize twice
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
