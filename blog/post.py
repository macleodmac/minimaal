
class Post(object):

    TEMPLATE = 'post.html'

    def __init__(self, config, content, metadata):
        self.config = config  # dict
        self.content = content  # markdown
        self.metadata = metadata  # dict

        # metadata contains:
        #   date: used to create url
        #   title: used to create url, page title
        #   excerpt: (optional) used to create precis
        #   tags: (optional) used to categorise posts

    @property
    def date(self):
        pass

    @property
    def title(self):
        pass

    @property
    def excerpt(self):
        pass

    @property
    def tags(self):
        pass

    @property
    def html(self):
        pass


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
