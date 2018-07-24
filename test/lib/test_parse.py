from unittest import TestCase

from lib.parse import split_meta_and_content, parse_metadata, make_string_url_friendly


class TestParse(TestCase):

    def test_split_meta_and_content_returns_blank_metadata_when_none_found(self):
        test_md = """*This is a test*"""

        meta, body = split_meta_and_content(test_md)

        self.assertEqual(meta, {})
        self.assertEqual(body, test_md)

    def test_split_meta_and_content_splits_metadata_and_body_correctly(self):
        test_md = """key: val\nkey2: val2\n\n*This is a test*\n#Test Header"""
        expected_meta = {'key': 'val', 'key2': 'val2'}
        expected_body = """*This is a test*\n#Test Header"""

        meta, body = split_meta_and_content(test_md)

        self.assertEqual(meta, expected_meta)
        self.assertEqual(body, expected_body)

    def test_parse_metadata_returns_empty_dict_for_empty_input(self):
        result = parse_metadata('')
        self.assertEqual(result, {})

    def test_parse_metadata_handles_multiple_lines_correctly(self):
        test_meta = """key: val\nkey2: val2\n"""
        expected = {'key': 'val', 'key2': 'val2'}

        actual = parse_metadata(test_meta)

        self.assertEqual(actual, expected)

    def test_make_string_url_friendly_handles_punctuation_correctly(self):
        text = "This is a test! You're ready to make this URL friendly?-   "
        expected = "this-is-a-test-youre-ready-to-make-this-url-friendly"

        actual = make_string_url_friendly(text)

        self.assertEqual(actual, expected)
