import logging
import os
import urllib.request

import yaml

from lib.parse import make_url_friendly

CSS_EXT = '.css'

BASE_CONFIG = {
    'base_url': 'http://www.test-blog.com',
    'posts_per_page': 10,
    'site_description': 'This is a site generated using minimaal',
    'md_ext': '.md',
    'date_format': '%d/%m/%Y',
    'site_title': 'My Blog',
    'directories': {
        'posts': 'posts',
        'output': 'output',
        'template': 'template',
    },
    'css': [
        'https://fonts.googleapis.com/css?family=Open+Sans:300',
        'https://cdn.rawgit.com/necolas/normalize.css/master/normalize.css',
        'https://cdn.rawgit.com/milligram/milligram/master/dist/milligram.min.css',
    ],
    'base_path': os.getcwd(),
}


def load_config_file(file_handle):
    return yaml.load(file_handle)


def build_config(user_config, base_config=BASE_CONFIG):
    base_config.update(user_config)
    return _normalise_config(base_config)


def _normalise_config(config):
    if config.get('base_url'):
        config['base_url'] = '/' + config['base_url'].lstrip('/')
    return config


def build_config_paths(config, base_dir):
    config['paths'] = {}
    for name, dir_path in config['directories'].items():
        config['paths'][name] = os.path.join(base_dir, dir_path)
    return config


def get_logger():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-4s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger('minimaal')


def get_css_paths(config, destination):
    # TODO: test
    all_paths = []
    for path in config.get('css', []):
        _, file_name = os.path.split(path)
        name, ext = os.path.splitext(file_name)
        ext = ext if ext else '.css'
        local_path = os.path.join(destination, file_name)
        urllib.request.urlretrieve(path, local_path)
        rel_path = os.path.relpath(destination, config['paths']['output'])
        cleaned_file_name = make_url_friendly(name) + ext
        relative_path = os.path.join(config.get('base_url'), rel_path, cleaned_file_name)
        all_paths.append(relative_path)
    return all_paths
