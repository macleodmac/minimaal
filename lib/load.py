import os

# TODO test
def read_path_contents(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    return text


def get_paths_with_ext(root, ext='.md'):
    all_paths = []
    for directory, _, files in os.walk(root):
        paths = [
            os.path.join(directory, f) for f in files
            if f.endswith(ext)
        ]
        all_paths.extend(paths)
    return all_paths
