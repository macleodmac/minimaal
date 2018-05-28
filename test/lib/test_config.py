from io import StringIO
from unittest import TestCase

from lib.config import load_config_file, build_config


class TestConfig(TestCase):

    def test_load_config_file_returns_dict(self):
        yaml = """
        key: val
        key2: val2
        list1:
          - el1
          - el2
          - el3
        """
        handle = StringIO()
        handle.writelines(yaml)
        handle.seek(0)

        actual = load_config_file(handle)

        expected = {
            'key': 'val',
            'key2': 'val2',
            'list1': [
                'el1',
                'el2',
                'el3',
            ],
        }
        self.assertEqual(expected, actual)

    def test_build_config_favours_user_config_over_base_config(self):
        base_config = {'foo': 'base_foo', 'bar': 'base_bar'}
        user_config = {'foo': 'user_foo', 'baz': 'user_baz'}

        actual = build_config(user_config, base_config)

        expected = {
            'foo': 'user_foo',
            'bar': 'base_bar',
            'baz': 'user_baz',
        }

        self.assertEqual(actual, expected)