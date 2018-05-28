import logging
import os
import re
import urllib.request

import yaml


BASE_CONFIG = {
    'base_url': 'http://www.test-blog.com',
    'posts_per_page': 10,
    'site_description': 'This is a site generated using minimaal',
    'md_ext': '.md',
    'date_format': '%d/%m/%Y',
    'posts_directory': 'posts',
    'output_directory': 'output',
    'template_directory': 'template',
    'site_title': 'My Blog',
}


def load_config_file(file_handle):
    return yaml.load(file_handle)


def build_config(user_config, base_config=BASE_CONFIG):
    base_config.update(user_config)
    return base_config


def get_logger():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-4s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger('minimaal')


def download_css_paths(paths, destination):
    # TODO: test
    all_paths = []
    for path in paths:
        _, file_name = os.path.split(path)
        file_name, _ = os.path.splitext(file_name)
        file_name = re.sub('[^0-9a-zA-Z.]+', '_', file_name).lower()
        local_path = os.path.join(destination, file_name + '.css')
        urllib.request.urlretrieve(path, local_path)
        all_paths.append(local_path)
    return all_paths
