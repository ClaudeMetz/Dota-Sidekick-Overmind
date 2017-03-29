from .handler import Handler
from ..crawler.items import ItemCrawler

import os.path


# Populates the databases for all languages
def populate(overseer, cacher, patch):
    for language in overseer.languages:
        db_path = os.path.join(overseer.tmp_path, "db", language, "new.db")
        with Handler(db_path) as handler:
            ItemCrawler(handler, cacher, overseer.lang_shorthand[language], patch).crawl()
            # etc
