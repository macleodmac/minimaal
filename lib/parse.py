import markdown2
import re
import yaml

""" Expects:
meta_1: value
meta_2: value

This is the *body* text
"""
META_PATTERN = re.compile(r'((?:\w+:.*\n)+)+', re.U)
META_DELIMITER = ':'


def read_and_split(file_path):
    with open(file_path, encoding='utf-8') as f:
        contents = f.read()
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


def parse_metadata(meta_text):
    return yaml.load(meta_text) or {}




