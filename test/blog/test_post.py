import datetime
from unittest import TestCase

from blog.post import Post


class TestParse(TestCase):

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
            jinja_env=None,
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

    def test_html(self):
        # TODO
        pass

    def test_html_content(self):
        # TODO
        pass

    def test_path_returns_well_formed_year_date_title(self):
        self.post.metadata.update({
            'title': "This! It's a test title.",
            'date': '20/09/2016',
        })
        expected = '2016/09/this-it-s-a-test-title.html'
        self.assertEqual(self.post.path, expected)

    def test_tags(self):
        # TODO
        pass

    def test_template(self):
        # TODO
        pass

    def test_title_returns_expected_value_from_metadata(self):
        test_title = "This! It's a test title."
        self.post.metadata.update({
            'title': test_title,
        })
        self.assertEqual(self.post.title, test_title)

    def test_title_url_friendly_strips_non_alphanumeric_characters(self):
        examples = {
            "Test Post - make sure you're into markdown!":
                "test-post-make-sure-you-re-into-markdown",
            "What's so great about this package? Good question.":
                "what-s-so-great-about-this-package-good-question",
            "Tests, and other ways to ensure code quality.":
                "tests-and-other-ways-to-ensure-code-quality",
        }
        for example, expected in examples.items():
            self.post.metadata.update({
                'title': example,
            })
            self.assertEqual(self.post.title_url_friendly, expected)

    def test_url(self):
        # TODO
        pass
