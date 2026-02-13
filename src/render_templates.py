from jinja2 import Environment, FileSystemLoader

base_path = 'src/templates'

def render_template(template_path: str, **kwargs):
    env = Environment(loader=FileSystemLoader(base_path))
    template = env.get_template(template_path)
    return template.render(kwargs)
