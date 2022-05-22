from jinja2 import Environment, PackageLoader, FileSystemLoader, ChoiceLoader


class Piggy:
    "A container object to be passed into jinja2 render as 'piggy'."
    def __init__(self, issues_list, labels_to_issues, config_d):
        self.config = config_d
        self.issues_list = issues_list
        self.labels_to_issues = labels_to_issues

        self._init_jinja2()

    def _init_jinja2(self):
        "Initialize jinja2 template loading."
        site_loader = FileSystemLoader(self.config.site_templates)
        pkg_loader = PackageLoader("ribbity")
        env = Environment(
            loader = ChoiceLoader([site_loader, pkg_loader])
        )
        self.env = env

    def render(self, template_name, **vardict):
        "Render given template using 'vardict'. Adds 'piggy' object."
        render_d = dict(vardict)
        render_d['piggy'] = self
        render_d['config'] = self.config

        template = self.env.get_template(template_name)
        return template.render(**render_d)
