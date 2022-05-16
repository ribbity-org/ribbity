from jinja2 import Environment, PackageLoader


env = Environment(
    loader=PackageLoader("ribbity")
)


def render_md(md_name, variables):
    template = env.get_template(md_name)
    return template.render(**variables)
