

class BaseCrawler:
    def __init__(self, session, cacher, patch, revision):
        self.session = session
        self.cacher = cacher
        self.patch = patch
        self.revision = revision
