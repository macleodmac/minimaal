from unittest.mock import patch
from io import StringIO
from unittest import TestCase

from lib.load import get_paths_with_ext


class TestLoad(TestCase):

    def test_get_paths_with_ext_returns_expected_absolute_paths(self):
        mock_walk_return = [
            (
                '/test/dir/1',
                ['subdir'],
                ['post_1.md', 'unwanted_file.jpg', 'epic_post.md'],
            ),
            (
                '/test/dir/1/subdir',
                ['subsubdir'],
                ['readme.md', 'another_random_file.html', 'fun_post.md'],
            ),
        ]
        expected = [
            '/test/dir/1/post_1.md',
            '/test/dir/1/epic_post.md',
            '/test/dir/1/subdir/readme.md',
            '/test/dir/1/subdir/fun_post.md',
        ]

        with patch('os.walk') as mock_walk:
            mock_walk.return_value = mock_walk_return
            actual = get_paths_with_ext('mocked/root', ext='.md')

        self.assertEqual(expected, actual)

    def test_get_paths_with_ext_returns_empty_list_when_no_matching_paths(self):
        mock_walk_return = [
            (
                '/test/dir/1',
                ['subdir'],
                ['unwanted.html', 'unwanted_file.jpg', 'epic_post.epub'],
            ),
            (
                '/test/dir/1/subdir',
                ['subsubdir'],
                ['readme.xlsx', 'another_random_file.html', 'fun_post.docx'],
            ),
        ]

        with patch('os.walk') as mock_walk:
            mock_walk.return_value = mock_walk_return
            actual = get_paths_with_ext('mocked/root', ext='.md')

        self.assertEqual([], actual)
