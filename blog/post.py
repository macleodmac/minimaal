import datetime
import os
import re

import markdown2

from lib.decorators import cached_property


class Post(object):

    TEMPLATE_NAME = 'post.html'
    EXTENSION = '.html'
    EXCERPT_LENGTH = 140
    AVG_WPM = 200

    def __init__(self, config, content, metadata, jinja_env):
        self.config = config  # dict
        self.content = content  # markdown
        self.metadata = metadata  # dict
        self.jinja_env = jinja_env

        # metadata contains:
        #   date: used to create url
        #   title: used to create url, page title
        #   excerpt: (optional) used to create precis
        #   tags: (optional) used to categorise posts

    @cached_property
    def date(self):
        date_str = self.metadata.get('date')
        fmt = self.config.get('date_format')
        return datetime.datetime.strptime(date_str, fmt)

    @cached_property
    def date_pretty(self):
        return self.date.strftime("%B %d, %Y")

    @cached_property
    def excerpt(self):
        default = '%s...' % (self.content[:self.EXCERPT_LENGTH], )
        return self.metadata.get('excerpt', default)

    @cached_property
    def html(self):
        return self.template.render(
            title=self.metadata.get('title'),
            content=self.html_content,
            css=self.config.get('css'),
            tags=self.tags,
            date=self.date_pretty,
        )

    @cached_property
    def html_content(self):
        extras = {
            'fenced-code-blocks': {
                'cssclass': 'code',
                'classprefix': 'code-',
            },
        }
        return markdown2.markdown(self.content, extras=extras)

    @cached_property
    def path(self):
        file_name = '%s%s' % (self.title_url_friendly, self.EXTENSION)
        return os.path.join(
            str(self.date.year),
            str(self.date.month).zfill(2),
            file_name,
        )

    @cached_property
    def tags(self):
        tags = self.metadata.get('tags', [])
        tags = [tag.strip() for tag in tags.split(',')]
        return tags

    @property
    def template(self):
        return self.jinja_env.get_template(self.TEMPLATE_NAME)

    @property
    def title(self):
        return self.metadata.get('title')

    @cached_property
    def title_url_friendly(self):
        title = self.title.lower().strip()
        title = title.replace('\'','')
        title = re.sub('[^a-zA-Z\d]+', '-', title)
        return title.strip('-')

    @property
    def url(self):
        return os.path.join(
            self.config.get('base_url'),
            self.path,
        )

    @cached_property
    def word_count(self):
        return len(self.content.split())
