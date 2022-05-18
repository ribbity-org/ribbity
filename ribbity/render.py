from jinja2 import Environment, PackageLoader, FileSystemLoader, ChoiceLoader


site_loader = FileSystemLoader("site-templates")
pkg_loader = PackageLoader("ribbity")
env = Environment(
    loader=ChoiceLoader([site_loader, pkg_loader])
)


def render_md(md_name, variables):
    template = env.get_template(md_name)
    return template.render(**variables)
