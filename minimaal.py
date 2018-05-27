import argparse

import os
from pprint import pprint

import jinja2

from lib.load import get_paths_with_ext
from lib.config import load_config_file, download_css_paths, build_config, get_logger
from lib.parse import read_and_split

from blog.post import Post
from blog.index import Index, make_tag_indices

log = get_logger()

parser = argparse.ArgumentParser(description='Load some config file for minimaal')

base_dir = os.getcwd()
config_path = os.path.join(base_dir, 'config.yaml')

with open(config_path, encoding='utf-8') as config_file:
    user_config = load_config_file(config_file)
config = build_config(user_config)

pprint(config)
PATHS = {
    'output': os.path.join(base_dir, config['output_directory']),
    'posts': os.path.join(base_dir, config['posts_directory']),
    'template': os.path.join(base_dir, config['template_directory']),
}


paths = get_paths_with_ext(PATHS['posts'], config['md_ext'])

env = jinja2.Environment(loader=jinja2.FileSystemLoader(PATHS['template']))

static_path = os.path.join(PATHS['output'], 'static')

css_path = os.path.join(static_path, 'css')
os.makedirs(css_path, exist_ok=True)
css_paths = download_css_paths(
    paths=config.get('css', []),
    destination=css_path,
)
env.globals['css'] = css_paths
env.globals['site_title'] = config['site_title']
env.globals['site_description'] = config['site_description']

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
    post_output_dir = os.path.join(PATHS['output'], directory)
    post_output_path = os.path.join(post_output_dir, file_name)
    os.makedirs(post_output_dir, exist_ok=True)
    with open(post_output_path, 'w', encoding='utf-8') as output:
        log.info("Writing post %s to %s", post.title, post_output_path)
        post.render(output)
        print(post.excerpt)

index = Index(
    config=config,
    posts=all_posts,
    jinja_env=env,
    title='Home'
)
index_path = os.path.join(PATHS['output'], 'index.html')
with open(index_path, 'w', encoding='utf-8') as output:
    log.info("Writing index to %s", index_path)
    output.writelines(index.html)

tag_indices = make_tag_indices(
    config=config,
    posts=all_posts,
    jinja_env=env,
)

for index in tag_indices:
    os.makedirs(index.directory, exist_ok=True)
    with open(index.path, 'w', encoding='utf-8') as output:
        log.info("Writing index to %s", index.path)
        index.render(output)

