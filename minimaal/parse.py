import re
import yaml

""" Expects:
meta_1: value
meta_2: value

This is the *body* text
"""
META_PATTERN = re.compile(r'((?:\w+:.*\n)+)+', re.U)
META_DELIMITER = ':'


def split_meta_and_content(text):
    lines = text.splitlines()
    meta_end, body_start = _get_meta_end_body_start_indices(lines)
    meta_text, body_text = lines[:meta_end], lines[body_start:]
    meta_text = '\n'.join(meta_text)
    meta_dict = parse_metadata(meta_text)
    return meta_dict, '\n'.join(body_text)


# TODO cleanup, there must be a more elegant way of doing this
def _get_meta_end_body_start_indices(lines):
    _index = 0
    for i, line in enumerate(lines):
        if line.strip() == '':
            _index = i
            break
    if _index:
        return _index, _index + 1
    return 0, 0


def parse_metadata(meta_text):
    return yaml.load(meta_text) or {}


def make_string_url_friendly(text):
    text = text.lower()
    text = text.replace('\'', '')
    text = re.sub("[^a-zA-Z\d]+", '-', text)
    text = text.strip().strip('-')
    return text


