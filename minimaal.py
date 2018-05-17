import os
from lib.load import load_config_file, get_paths_with_ext
import jinja2
from lib.parse import read_and_split
from blog.post import Post

BASE_CONFIG = {
    'posts_per_page': 10,
    'description': 'This is a site generated using minimaal',
    'title': 'minimaal',
    'md_ext': '.md',
    'date_format': '%d/%m/%Y',
}
base_dir = '/home/jamie/Desktop/Projects/minimaal/'
config_path = os.path.join(base_dir, 'config.yaml')
posts_path = os.path.join(base_dir, 'posts')
output_path = os.path.join(base_dir, 'output')

with open(config_path, encoding='utf-8') as config_file:
    config = load_config_file(config_file)

md_ext = config.get('md_ext', BASE_CONFIG['md_ext'])

paths = get_paths_with_ext(posts_path, md_ext)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('/home/jamie/Desktop/Projects/minimaal/template'),
)

template = env.get_template('child.html')

for path in paths:
    metadata, content = read_and_split(path)
    post = Post(
        config=config,
        content=content,
        metadata=metadata,
        jinja_env=env,
    )
    directory, file_name = os.path.split(post.path)
    output_dir = os.path.join(output_path, directory)
    output_file = os.path.join(output_dir, file_name)
    os.makedirs(output_dir, exist_ok=True)
    print(output_file)
    with open(output_file, 'w', encoding='utf-8') as output:
        output.writelines(post.html)

print(paths)
print(config)
