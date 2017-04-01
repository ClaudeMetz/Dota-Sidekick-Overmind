

class BaseCrawler:
    def __init__(self, handler, cacher, patch, revision):
        self.handler = handler
        self.cacher = cacher
        self.patch = patch
        self.revision = revision
