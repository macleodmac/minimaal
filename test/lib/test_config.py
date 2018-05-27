from io import StringIO
from unittest import TestCase

from lib.config import load_config_file


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
