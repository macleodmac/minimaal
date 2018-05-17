import jinja2
from lib.parse import read_and_split, markdown_to_html, write_html_to_file
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('/home/jamie/Desktop/Projects/minimaal/template'),
)

template = env.get_template('child.html')

md, bd = read_and_split('/home/jamie/Desktop/Projects/minimaal/posts/why_minimaal.md')
print(md)

parsed = markdown_to_html(bd)
print(parsed)
html = template.render(title='title', body=parsed)

write_html_to_file('/home/jamie/Desktop/Projects/minimaal/output.html', html)

