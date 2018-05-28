import datetime
from unittest import TestCase
from unittest.mock import Mock
from blog.index import Index, TagIndex, make_tag_indices
from blog.post import Post


class TestIndex(TestCase):

    # def setUp(self):
    #     self.metadata = {
    #         'title': 'This: is the post title!',
    #         'date': '29/09/2017',
    #         'excerpt': 'This is the excerpt of the post.',
    #     }
    #     self.content = """# This is a test
    #     * I hope you like reading markdown.
    #     * If not, you're out of luck!"""
    #     self.config = {
    #         'date_format': '%d/%m/%Y',
    #     }
    #     self.post = Post(
    #         config=self.config,
    #         content=self.content,
    #         metadata=self.metadata,
    #         jinja_env=Mock(),
    #     )

    @staticmethod
    def _post_with_tags(tags):
        return Post(
            config={},
            content='Test content',
            metadata={'tags': tags},
            jinja_env=Mock(),
        )

    @staticmethod
    def _get_index_by_title(indices, title):
        return next((i for i in indices if i.title == title), None)

    def test_index_len_returns_number_of_posts(self):
        posts = [None] * 5
        index = Index(config={}, posts=posts, jinja_env=Mock(), title='Test')
        self.assertEqual(len(index), len(posts))

    def test_index_path_is_index_html(self):
        index = Index(config={}, posts=[], jinja_env=Mock(), title='Test')
        self.assertEqual(index.path, 'index.html')
        self.assertEqual(index.title, 'Test')

    def test_tag_index_path_is_valid_string(self):
        tag_name = 'Tag Name'
        index = TagIndex(config={}, posts=[], jinja_env=Mock(), title=tag_name)
        expected_path = 'tags/tag-name.html'
        self.assertEqual(index.path, expected_path)

    def test_make_tag_indices_groups_posts_correctly(self):
        posts = [
            self._post_with_tags('foo'),
            self._post_with_tags('bar'),
            self._post_with_tags('foo, bar'),
            self._post_with_tags('baz'),
        ]

        indices = make_tag_indices(config={}, posts=posts, jinja_env=Mock())

        self.assertEqual(len(indices), 3)
        self.assertListEqual(
            sorted([index.title for index in indices]),
            sorted(['foo', 'bar', 'baz']),
        )

        foo_index = self._get_index_by_title(indices, 'foo')
        self.assertEqual(len(foo_index), 2)

        bar_index = self._get_index_by_title(indices, 'bar')
        self.assertEqual(len(bar_index), 2)

        baz_index = self._get_index_by_title(indices, 'baz')
        self.assertEqual(len(baz_index), 1)
