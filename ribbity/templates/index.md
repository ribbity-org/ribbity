# Welcome to the {site_name}!

This page is made from a generic jinja2 template that comes with ribbity.

You can see [the template here](https://github.com/ctb/ribbity/blob/main/ribbity/templates/index.md).

Make a copy, put it in `./site-templates`, and edit it for your own project!

## Start here!

{% for issue in issues_list %}
{% if issue.is_frontpage %}

[Example: {{issue.title}}]({{issue.output_filename}})

{% endif %}
{% endfor %}

---

## [All examples](examples.md)

---

## [All categories](labels.md)

