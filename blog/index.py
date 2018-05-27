from collections import defaultdict
import os
from lib.parse import make_url_friendly
from lib.mixin import RenderFileMixin


class Index(RenderFileMixin):

    TEMPLATE_NAME = 'index-home.html'
    EXTENSION = '.html'

    def __init__(self, config, posts, jinja_env, title):
        self.config = config
        self.posts = posts
        self.template = jinja_env.get_template(self.TEMPLATE_NAME)
        self.title = title

    @property
    def path(self):
        return 'index' + self.EXTENSION

    @property
    def html(self):
        return self.template.render(
            title=self.title,
            posts=self.posts,
        )


class TagIndex(Index):

    TEMPLATE_NAME = 'index-tag.html'

    @property
    def path(self):
        title = make_url_friendly(self.title)
        return os.path.join('tags', title + self.EXTENSION)


def make_tag_indices(config, posts, jinja_env):
    # TODO: test
    all_indexes = []
    grouped_by_tag = defaultdict(list)
    for post in posts:
        for tag in post.tags:
            grouped_by_tag[tag].append(post)
    for tag, posts in grouped_by_tag.items():
        all_indexes.append(
            TagIndex(
                config=config,
                posts=posts,
                jinja_env=jinja_env,
                title=tag,
            )
        )
    return all_indexes
