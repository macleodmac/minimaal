import tempfile

from unittest import TestCase

from lib.load import load_config, get_paths_with_ext


class TestLoad(TestCase):

    def test_load_config_returns_dict(self):
        yaml = """
        key: val
        key2: val2
        list1:
          - el1
          - el2
          - el3
        """
        with tempfile.NamedTemporaryFile(mode='w') as tf:
            tf.writelines(yaml.splitlines())
            actual = load_config(tf.name)

        expected = {
            'key': 'val',
            'key2': 'val2',
            'list1': [
                'el1,'
                'el2',
                'el3',
            ],
        }
        self.assertEqual(expected, actual)
