from .handler import Handler
from ..crawler.items import ItemCrawler
from ..crawler.heroes import HeroCrawler

import os.path
from bs4 import BeautifulSoup


# Populates the databases for all languages
def populate(overseer, cacher, patch):
    for language in overseer.languages:
        db_path = os.path.join(overseer.tmp_path, "db", language, "new.db")
        with Handler(db_path) as handler:
            item_list = list_items(cacher)
            ItemCrawler(handler, cacher, overseer.lang_shorthand[language], patch).crawl(item_list)
            HeroCrawler(handler, cacher, overseer.lang_shorthand[language], patch).crawl()


# Returns a list with the names of all available items
def list_items(cacher):
    html = cacher.get("https://www.dotabuff.com/items")
    soup = BeautifulSoup(html, "lxml")

    raw_list = soup.find_all(class_="cell-xlarge")
    clean_list = []
    for item in raw_list:
        clean_list.append(str(item.a["href"][7:]))
    return clean_list
