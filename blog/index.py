
class Index(object):

    TEMPLATE = 'index.html'

    def __init__(self, config, posts):
        self.config = config
        self.posts = posts

    @property
    def html(self):
        all_html = ''
        for post in self.posts:
            all_html += post.html
        return all_html

    def render(self, file_handle):
        file_handle.writelines(self.html)



class TagIndex(Index):

    TEMPLATE = 'tag-index.html'

    def __init__(self, config, posts):
        self.config = config
        self.posts = posts
