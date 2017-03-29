from .handler import Handler
from ..crawler.items import crawl_items

import os.path


# Populates the databases for all languages
def populate(overseer, cacher):
    for language in overseer.languages:
        db_path = os.path.join(overseer.tmp_path, "db", language, "new.db")
        with Handler(db_path) as handler:
            crawl_items(handler, cacher, overseer.lang_shorthand[language])
            # etc
