import markdown2
import datetime
import os
import re


class Post(object):

    TEMPLATE_NAME = 'post.html'

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

    @property
    def date(self):
        date_str = self.metadata.get('date')
        fmt = self.config.get('date_format')
        return datetime.datetime.strptime(date_str, fmt)

    @property
    def title(self):
        return self.metadata.get('title')

    @property
    def url(self):
        pass

    @property
    def url_friendly_title(self):
        title = self.title.lower().strip()
        title = re.sub('[^a-zA-Z\d]+', '-', title)
        title = title.strip('-')
        return title

    @property
    def path(self):
        return os.path.join(
            str(self.date.year),
            str(self.date.month).zfill(2),
            self.url_friendly_title + '.html',
        )

    @property
    def excerpt(self):
        pass

    @property
    def tags(self):
        pass

    @property
    def template(self):
        return self.jinja_env.get_template(self.TEMPLATE_NAME)

    @property
    def html_content(self):
        extras = {
            'fenced-code-blocks': {
                'cssclass': 'code',
                'classprefix': 'code-',
            },
        }
        return markdown2.markdown(self.content, extras=extras)

    @property
    def html(self):
        return self.template.render(title='title', content=self.html_content)


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
