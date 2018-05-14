import os
import yaml


# TODO: Refactor to use file handles
def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.load(f)
    return config


def get_paths_with_ext(root, ext='.md'):
    all_paths = []
    for directory, _, files in os.walk(root):
        all_paths.extend([
            os.path.join(directory, f) for f in files
            if f.endswith(ext)
        ])
    return all_paths
