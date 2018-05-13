import markdown2
import re


META_PATTERN = re.compile(r'(?:\s*\n)*((?:\w+:.*\n)+)(?:\s*\n)+.*', re.U)
META_DELIMITER = ':'

MARKDOWN2_EXTRAS = {
    'fenced-code-blocks': {
        'cssclass': 'code',
        'classprefix': 'code-',
    },
}


def parse_to_markdown(text, extras=MARKDOWN2_EXTRAS):
    return markdown2.markdown(text, extras=extras)


def read_and_split(file_path):
    contents = read_file_from_path(file_path)
    return split_markdown(contents)


def split_markdown(text, meta_pattern=META_PATTERN):
    metadata = {}
    matched = meta_pattern.match(text)
    if not matched:
        return metadata, text

    meta_items = matched.group(1).splitlines()
    metadata = parse_metadata(meta_items)
    body = text[matched.end():]
    return metadata, body


def parse_metadata(items, meta_delimiter=META_DELIMITER):
    metadata = {}
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


#
# md, bd = read_and_split('/home/jamie/Desktop/Projects/Letterpress/press/sample_post.md')
# parsed = parse_to_markdown(bd)
# print(parsed)
# with open('/home/jamie/Desktop/test.html', 'w') as f:
#     f.writelines(parsed)
