

class BaseCrawler:
    def __init__(self, cacher, patch, revision):
        self.cacher = cacher
        self.patch = patch
        self.revision = revision
