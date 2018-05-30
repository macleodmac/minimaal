import datetime
import os

import markdown2

from lib.decorators import cached_property
from lib.parse import make_url_friendly
from blog.render import RenderFileMixin


class Post(RenderFileMixin):

    TEMPLATE_NAME = 'post.html'
    EXTENSION = '.html'
    EXCERPT_LENGTH = 140

    def __init__(self, config, content, metadata, jinja_env):
        self.config = config
        self.content = content
        self.metadata = metadata
        self.template = jinja_env.get_template(self.TEMPLATE_NAME)

    @cached_property
    def date(self):
        date_str = self.metadata.get('date')
        fmt = self.config.get('date_format')
        return datetime.datetime.strptime(date_str, fmt)

    @property
    def pretty_date(self):
        return self.date.strftime("%B %d, %Y")

    @cached_property
    def excerpt(self):
        default = '%s...' % (self.content[:self.EXCERPT_LENGTH], )
        return self.metadata.get('excerpt', default)

    @cached_property
    def html(self):
        extras = {
            'fenced-code-blocks': {
                'cssclass': 'code',
                'classprefix': 'code-',
            },
        }
        content = markdown2.markdown(self.content, extras=extras)
        return self.template.render(
            content=content,
            post=self,
        )

    @cached_property
    def path(self):
        title = make_url_friendly(self.title)
        return os.path.join(
            str(self.date.year),
            str(self.date.month).zfill(2),
            title + self.EXTENSION,
        )

    @cached_property
    def tags(self):
        tags = self.metadata.get('tags', [])
        if tags:
            tags = [tag.strip() for tag in tags.split(',')]
        return list(filter(None, tags))

    @property
    def title(self):
        return self.metadata.get('title')

    @property
    def url(self):
        return '/' + os.path.join(
            self.config.get('base_url'),
            self.path,
        )
