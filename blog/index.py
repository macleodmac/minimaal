from collections import defaultdict
import os
from lib.parse import make_url_friendly
from blog.render import RenderFileMixin


class Index(RenderFileMixin):

    TEMPLATE_NAME = 'index-home.html'
    EXTENSION = '.html'

    def __init__(self, config, posts, jinja_env, title):
        # TODO: add super call
        self.config = config
        self.posts = posts
        self.template = jinja_env.get_template(self.TEMPLATE_NAME)
        self.title = title

    def __len__(self):
        return len(self.posts)

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
    grouped = _group_posts_by_tag(posts)
    return [
        TagIndex(
            config=config,
            posts=posts,
            jinja_env=jinja_env,
            title=tag,
        ) for tag, posts in grouped.items()
    ]


def _group_posts_by_tag(posts):
    grouped = defaultdict(list)
    for post in posts:
        for tag in post.tags:
            grouped[tag].append(post)
    return grouped
