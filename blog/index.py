
class Index(object):

    TEMPLATE_NAME = 'index.html'

    def __init__(self, config, posts, jinja_env):
        self.config = config
        self.posts = posts
        self.template = jinja_env.get_template(self.TEMPLATE_NAME)

    @property
    def html(self):
        return self.template.render(
            title='Title',
            posts=self.posts,
        )


class TagIndex(Index):

    TEMPLATE = 'tag-index.html'
