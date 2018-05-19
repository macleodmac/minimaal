from unittest import TestCase
from unittest.mock import Mock
from lib.decorators import cached_property


class TestDecorators(TestCase):

    def test_cached_property_is_cached(self):

        class TestClass(object):
            def __init__(self):
                self.mock_fn = Mock()

            @cached_property
            def test_property(self):
                return self.mock_fn()

        test_class = TestClass()

        self.assertEqual(test_class.mock_fn.call_count, 0)
        test_class.test_property
        self.assertEqual(test_class.mock_fn.call_count, 1)
        test_class.test_property
        test_class.test_property
        test_class.test_property
        self.assertEqual(test_class.mock_fn.call_count, 1)
