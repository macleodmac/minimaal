

class Index(object):

    TEMPLATE = 'index.html'

    def __init__(self, config, posts):
        self.config = config
        self.posts = posts


class TagIndex(Index):

    TEMPLATE = 'tag-index.html'

    def __init__(self, config, posts):
        self.config = config
        self.posts = posts
