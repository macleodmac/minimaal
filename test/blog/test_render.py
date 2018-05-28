import io
from unittest import TestCase
from blog.render import RenderFileMixin


class TestRender(TestCase):

    class TestRenderFile(RenderFileMixin):

        @property
        def path(self):
            return 'my/test/dir/path'

        @property
        def html(self):
            return '<h1>Test HTML</h1>\n<p>Test paragraph</p>'

    def test_mixin_raises_exception_for_directory_and_html(self):
        test_class = RenderFileMixin()
        with self.assertRaises(NotImplementedError):
            test_class.directory
        with self.assertRaises(NotImplementedError):
            test_class.html

    def test_subclassed_mixin_returns_directory_correctly(self):
        test_class = self.TestRenderFile()
        expected = 'my/test/dir'
        self.assertEqual(test_class.directory, expected)

    def test_subclassed_mixin_renders_file_html_correctly(self):
        test_class = self.TestRenderFile()
        buffer = io.StringIO()

        test_class.render(buffer)

        output_lines = buffer.getvalue().splitlines()
        self.assertEqual(output_lines[0], '<h1>Test HTML</h1>')
        self.assertEqual(output_lines[1], '<p>Test paragraph</p>')
