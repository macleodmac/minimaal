import markdown2
import re

""" Expects:
meta_1: value
meta_2: value

This is the *body* text
"""
META_PATTERN = re.compile(r'((?:\w+:.*\n)+)+', re.U)
META_DELIMITER = ':'

MARKDOWN2_EXTRAS = {
    'fenced-code-blocks': {
        'cssclass': 'code',
        'classprefix': 'code-',
    },
}


def markdown_to_html(text, extras=MARKDOWN2_EXTRAS):
    return markdown2.markdown(text, extras=extras)


def read_and_split(file_path):
    contents = read_file_from_path(file_path)
    meta_text, body_text = split_markdown(contents)
    meta_dict = parse_metadata(meta_text)
    return meta_dict, body_text


def split_markdown(text, meta_pattern=META_PATTERN):
    matched = meta_pattern.match(text)
    if not matched:
        return '', text
    meta_block = matched.group(1)
    body = text[matched.end():].lstrip()
    return meta_block, body


def parse_metadata(meta_text, meta_delimiter=META_DELIMITER):
    metadata = {}
    items = meta_text.splitlines()
    for item in items:
        key, val = item.split(meta_delimiter, 1)
        val = val.strip()
        if val:
            metadata[key.strip()] = val
    return metadata


def read_file_from_path(file_path):
    with open(file_path, encoding='utf-8') as f:
        contents = f.read()
    return contents


def write_html_to_file(file_path, contents):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(contents)





