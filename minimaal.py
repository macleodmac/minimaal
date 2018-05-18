import os
from pprint import pprint

import jinja2

from lib.load import load_config_file, get_paths_with_ext
from lib.parse import read_and_split

from blog.post import Post


BASE_CONFIG = {
    'base_url': 'http://www.test-blog.com',
    'posts_per_page': 10,
    'description': 'This is a site generated using minimaal',
    'title': 'minimaal',
    'md_ext': '.md',
    'date_format': '%d/%m/%Y',
    'posts_directory': 'posts',
    'output_directory': 'output',
    'template_directory': 'template',
}

base_dir = '/home/jamie/Desktop/Projects/minimaal/'
config_path = os.path.join(base_dir, 'config.yaml')

with open(config_path, encoding='utf-8') as config_file:
    user_config = load_config_file(config_file)

config = BASE_CONFIG

config.update(user_config)
pprint(config)
posts_path = os.path.join(base_dir, config['posts_directory'])
output_path = os.path.join(base_dir, config['output_directory'])
template_path = os.path.join(base_dir, config['template_directory'])

paths = get_paths_with_ext(posts_path, config['md_ext'])

env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))

for path in paths:
    metadata, content = read_and_split(path)
    post = Post(
        config=config,
        content=content,
        metadata=metadata,
        jinja_env=env,
    )
    directory, file_name = os.path.split(post.path)
    post_output_dir = os.path.join(output_path, directory)
    post_output_path = os.path.join(post_output_dir, file_name)
    os.makedirs(post_output_dir, exist_ok=True)
    with open(post_output_path, 'w', encoding='utf-8') as output:
        output.writelines(post.html)
