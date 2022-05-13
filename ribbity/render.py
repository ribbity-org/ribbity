from jinja2 import Environment, ChoiceLoader, FileSystemLoader


env = Environment(
    loader=ChoiceLoader([FileSystemLoader('./pages')]),
)


def render_md(md_name, variables):
    template = env.get_template(md_name)
    return template.render(**variables)
