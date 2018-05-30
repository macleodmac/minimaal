import datetime
from unittest import TestCase
from unittest.mock import Mock
from blog.post import Post


class TestPost(TestCase):

    def setUp(self):
        self.metadata = {
            'title': 'This: is the post title!',
            'date': '29/09/2017',
            'excerpt': 'This is the excerpt of the post.',
        }
        self.content = """# This is a test
        * I hope you like reading markdown.
        * If not, you're out of luck!"""
        self.config = {
            'date_format': '%d/%m/%Y',
        }
        self.post = Post(
            config=self.config,
            content=self.content,
            metadata=self.metadata,
            jinja_env=Mock(),
        )

    def test_date_is_valid_datetime_object(self):
        self.post.metadata.update({'date': '20/09/2016'})
        expected = datetime.datetime(2016, 9, 20)
        self.assertEqual(self.post.date, expected)

    def test_excerpt_is_returned_when_specified_in_metadata(self):
        test_excerpt = 'This is a test excerpt'
        self.post.metadata.update({
            'excerpt': test_excerpt,
        })
        self.assertEqual(self.post.excerpt, test_excerpt)

    def test_content_is_returned_when_no_excerpt_specified_in_metadata(self):
        test_content = 'This is a test. I hope you like markdown!'
        del self.post.metadata['excerpt']
        self.post.content = test_content

        self.assertEqual(self.post.excerpt, test_content + '...')

    def test_path_returns_well_formed_year_date_title(self):
        self.post.metadata.update({
            'title': "This! It's a test title.",
            'date': '20/09/2016',
        })
        expected = '2016/09/this-its-a-test-title.html'
        self.assertEqual(self.post.path, expected)

    def test_tags_returns_populated_list_from_metadata_delimited_list(self):
        self.post.metadata.update({
            'tags': "technology, python, learning",
        })
        expected = ['technology', 'python', 'learning']
        self.assertEqual(self.post.tags, expected)

    def test_tags_returns_discards_empty_tags_when_misspecified(self):
        self.post.metadata.update({
            'tags': ", python, learning,",
        })
        expected = ['python', 'learning']
        self.assertEqual(self.post.tags, expected)

    def test_tags_returns_empty_list_when_no_specified_tags(self):
        self.assertEqual(self.post.tags, [])

    def test_title_returns_expected_value_from_metadata(self):
        test_title = "This! It's a test title."
        self.post.metadata.update({
            'title': test_title,
        })
        self.assertEqual(self.post.title, test_title)

    def test_url_is_correctly_formed_from_config_date_and_title(self):
        test_title = "Test Post - make sure you're into markdown!"
        self.post.metadata.update({
            'title': test_title,
            'date': '10/05/2018',
        })
        self.post.config.update({
            'base_url': 'basetest',
        })
        expected = '/basetest/2018/05/test-post-make-sure-youre-into-markdown.html'
        self.assertEqual(self.post.url, expected)
