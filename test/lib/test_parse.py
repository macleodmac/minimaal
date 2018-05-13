from unittest import TestCase

from lib.parse import markdown_to_html, split_markdown, parse_metadata


class TestParse(TestCase):

    def test_parse_to_markdown_returns_valid(self):
        test_md = """*This is a test*"""
        expected = """<p><em>This is a test</em></p>"""

        parsed = markdown_to_html(test_md)

        actual = parsed.splitlines()[0]
        self.assertEqual(expected, actual)

    def test_split_markdown_returns_blank_metadata_when_none_found(self):
        test_md = """*This is a test*"""

        meta, body = split_markdown(test_md)

        self.assertEqual(meta, '')
        self.assertEqual(body, test_md)

    def test_split_markdown_splits_metadata_and_body_correctly(self):
        test_md = """key: val\nkey2: val2\n*This is a test*"""
        expected_meta = """key: val\nkey2: val2\n"""
        expected_body = """*This is a test*"""

        meta, body = split_markdown(test_md)

        self.assertEqual(meta, expected_meta)
        self.assertEqual(body, expected_body)

    def test_parse_metadata_returns_empty_for_empty_string(self):
        result = parse_metadata('')
        self.assertEqual(result, {})

    def test_parse_metadata_handles_multiple_lines_correctly(self):
        test_meta = """key: val\nkey2: val2\n"""
        expected = {'key': 'val', 'key2': 'val2'}

        actual = parse_metadata(test_meta)

        self.assertEqual(actual, expected)



