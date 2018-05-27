import os


def get_paths_with_ext(root, ext='.md'):
    all_paths = []
    for directory, _, files in os.walk(root):
        paths = [
            os.path.join(directory, f) for f in files
            if f.endswith(ext)
        ]
        all_paths.extend(paths)
    return all_paths
