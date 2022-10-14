# All categories

*Go to: [Home](index.md) | [All examples](examples.md)*

---

{% for label in labels_to_issues %}

[{{label.description or label.name}} - {{labels_to_issues[label]|length}} examples]({{label.output_filename}})

{% endfor %}
