

class BaseCrawler:
    def __init__(self, handler, cacher, lang_shorthand, patch):
        self.handler = handler
        self.cacher = cacher
        self.lang_shorthand = lang_shorthand
        self.patch = patch
