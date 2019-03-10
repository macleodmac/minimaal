from unittest.mock import Mock
from minimaal.model.index import Index, TagIndex, make_tag_indices
from minimaal.model.post import Post


def _post_with_tags(tags):
    return Post(
        config={},
        content='Test content',
        metadata={'tags': tags},
        jinja_env=Mock(),
    )


def _get_index_by_title(indices, title):
    return next((i for i in indices if i.title == title), None)


def test_index_len_returns_number_of_posts():
    posts = [None] * 5
    index = Index(config={}, posts=posts, jinja_env=Mock(), title='Test')
    assert len(index) == len(posts)


def test_index_path_is_index_html():
    index = Index(config={}, posts=[], jinja_env=Mock(), title='Test')
    assert index.path == 'index.html'
    assert index.title == 'Test'


def test_tag_index_path_is_valid_string():
    tag_name = 'Tag Name'
    index = TagIndex(config={}, posts=[], jinja_env=Mock(), title=tag_name)
    expected_path = 'tags/tag-name.html'
    assert index.path == expected_path


def test_make_tag_indices_groups_posts_correctly():
    posts = [
        _post_with_tags('foo'),
        _post_with_tags('bar'),
        _post_with_tags('foo, bar'),
        _post_with_tags('baz'),
    ]

    indices = make_tag_indices(config={}, posts=posts, jinja_env=Mock())

    assert len(indices) == 3
    assert sorted([index.title for index in indices]) == sorted(['foo', 'bar', 'baz'])

    foo_index = _get_index_by_title(indices, 'foo')
    assert len(foo_index) == 2

    bar_index = _get_index_by_title(indices, 'bar')
    assert len(bar_index) == 2

    baz_index = _get_index_by_title(indices, 'baz')
    assert len(baz_index) == 1
