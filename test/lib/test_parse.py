from unittest import TestCase

from lib.parse import parse_to_markdown, split_markdown


class TestParse(TestCase):

    def test_parse_to_markdown_returns_valid(self):
        test_md = """*This is a test*"""
        expected = """<p><em>This is a test</em></p>"""

        parsed = parse_to_markdown(test_md)

        actual = parsed.splitlines()[0]
        self.assertEqual(expected, actual)

    def test_split_markdown_file_returns_empty_metadata_when_none_found(self):
        test_md = """*This is a test*"""

        meta, body = split_markdown(test_md)

        self.assertEqual(meta, {})
        self.assertEqual(body, test_md)

    def test_split_markdown_file_splits_metadata_and_body_correctly(self):
        test_md = r"""key: val
        *This is a test*
        """

        meta, body = split_markdown(test_md)

        self.assertEqual(meta, {})
        self.assertEqual(body, test_md)


