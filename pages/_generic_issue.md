# {{issue.output_title}}

*[{{github_repo}}#{{issue.number}}](https://github.com/{{github_repo}}/issues/{{issue.number}})*

---

{{body}}

{% if issue.labels %}
## Categories

This example has the following categories:

{% for label in issue.labels %} * [{{label.output_name}}]({{label.output_filename}})
{% endfor %}

{% endif %}
