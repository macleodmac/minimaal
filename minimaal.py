import argparse

import os
from pprint import pprint

import jinja2

from lib.load import get_paths_with_ext
from lib.config import load_config_file, get_css_paths, build_config, build_config_paths, get_logger
from lib.parse import read_and_split

from blog.post import Post
from blog.index import Index, make_tag_indices

log = get_logger()


def build_posts(config, post_paths, jinja_env):
    all_posts = []
    for path in post_paths:
        metadata, content = read_and_split(path)
        post = Post(
            config=config,
            content=content,
            metadata=metadata,
            jinja_env=jinja_env,
        )
        all_posts.append(post)
    return all_posts


def build_index(config, posts, jinja_env):
    index = Index(
        config=config,
        posts=posts,
        jinja_env=jinja_env,
        title='Home',
    )
    return index


def build_tag_indices(config, posts, jinja_env):
    tag_indices = make_tag_indices(
        config=config,
        posts=posts,
        jinja_env=jinja_env,
    )
    return tag_indices


def render(config, items):
    for item in items:
        output_dir = os.path.join(config['paths']['output'], item.directory)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(config['paths']['output'], item.path)
        with open(output_path, 'w', encoding='utf-8') as output:
            log.info("Writing file to %s", item.path)
            item.render(output)


def make_config():
    # parser = argparse.ArgumentParser(description='Load some config file for minimaal')

    base_path = os.getcwd()
    config_path = os.path.join(base_path, 'config.yaml')

    with open(config_path, encoding='utf-8') as config_file:
        user_config = load_config_file(config_file)

    config = build_config(user_config)
    config = build_config_paths(config, base_path)

    pprint(config)

    return config


def make_jinja_env(config):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(config['paths']['template']))
    css_output_dir = os.path.join(config['paths']['output'], 'static', 'css')
    os.makedirs(css_output_dir, exist_ok=True)
    css = get_css_paths(
        config=config,
        destination=css_output_dir,
    )
    print(css)
    env.globals.update({
        'css': css,
        'config': config,
    })
    return env


def run():
    config = make_config()
    jinja_env = make_jinja_env(config)
    post_paths = get_paths_with_ext(
        root=config['paths']['posts'],
        ext=config['md_ext'],
    )
    posts = build_posts(config, post_paths, jinja_env)
    index = build_index(config, posts, jinja_env)
    tag_indices = build_tag_indices(config, posts, jinja_env)
    all_items = posts + tag_indices + [index]
    render(config=config, items=all_items)


run()