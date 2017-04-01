from .handler import Handler
from ..organizer.cacher import Cacher
from ..crawler.items import ItemCrawler
from ..crawler.heroes import HeroCrawler

import os.path
from bs4 import BeautifulSoup


# Populates the databases for all languages
def populate(overseer, patch):
    cacher = Cacher(overseer, "english")
    item_list = list_items(cacher)
    hero_list = list_heroes(cacher)
    for language in overseer.languages:
        db_path = os.path.join(overseer.tmp_path, "db", language, "new.db")
        if language != "english":  # So the www-cacher doesn't initialize twice
            cacher = Cacher(overseer, language)
        with Handler(db_path) as handler:
            ItemCrawler(handler, cacher, patch).crawl(item_list)
            HeroCrawler(handler, cacher, patch).crawl(hero_list)


# Returns a list with the names of all available items
def list_items(cacher):
    html = cacher.get("dotabuff.com/items")
    soup = BeautifulSoup(html, "lxml")

    raw_list = soup.find_all(class_="cell-xlarge")
    clean_list = []
    for item in raw_list:
        clean_list.append(str(item.a["href"][7:]))
    return clean_list


# Returns a list with the names of all available heroes
def list_heroes(cacher):
    html = cacher.get("dotabuff.com/heroes")
    soup = BeautifulSoup(html, "lxml")

    div = soup.find(class_="hero-grid")
    raw_list = div.find_all("a")
    clean_list = []
    for item in raw_list:
        clean_list.append(str(item["href"][8:]))
    return clean_list
