import argparse
import logging
import os
from pprint import pprint
import urllib.request
import re
import jinja2

from lib.load import load_config_file, get_paths_with_ext
from lib.parse import read_and_split

from blog.post import Post
from blog.index import Index

log = logging.getLogger(__name__)


LOG_FORMAT = '[%(asctime)s] %(levelname)-4s %(message)s'

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

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

# parser = argparse.ArgumentParser(description='Load some config file for minimaal')



base_dir = os.getcwd()
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

static_path = os.path.join(output_path, 'static')
css_path = os.path.join(static_path, 'css')

os.makedirs(css_path, exist_ok=True)
rel_url = 'minimaal'
css_paths = []
for css in config.get('css'):
    _, file_name = os.path.split(css)
    file_name, _ = os.path.splitext(file_name)
    file_name = re.sub('[^0-9a-zA-Z.]+', '_', file_name).lower()
    local_path = os.path.join(css_path, file_name + '.css')
    urllib.request.urlretrieve(css, local_path)
    rel_path = '/' + os.path.join(rel_url, os.path.relpath(local_path, output_path))
    print(css, rel_path)
    css_paths.append(rel_path)

env.globals['css'] = css_paths
all_posts = []
for path in paths:
    metadata, content = read_and_split(path)
    post = Post(
        config=config,
        content=content,
        metadata=metadata,
        jinja_env=env,
    )
    all_posts.append(post)

for post in all_posts:
    directory, file_name = os.path.split(post.path)
    post_output_dir = os.path.join(output_path, directory)
    post_output_path = os.path.join(post_output_dir, file_name)
    os.makedirs(post_output_dir, exist_ok=True)
    with open(post_output_path, 'w', encoding='utf-8') as output:
        log.info("Writing post %s to %s", post.title, post_output_path)
        output.writelines(post.html)
        print(post.excerpt)

index = Index(
    config=config,
    posts=all_posts,
    jinja_env=env,
)
index_path = os.path.join(output_path, 'index.html')
with open(index_path, 'w', encoding='utf-8') as output:
    log.info("Writing index to %s", index_path)
    output.writelines(index.html)
