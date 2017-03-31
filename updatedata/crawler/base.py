

class BaseCrawler:
    def __init__(self, handler, cacher, patch):
        self.handler = handler
        self.cacher = cacher
        self.patch = patch
