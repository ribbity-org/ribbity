{# receives 'issue', 'body', and 'piggy' #}
# {{config.issue_title_prefix}}{{issue.title}}

*[{{piggy.config.github_repo}}#{{issue.number}}](https://github.com/{{piggy.config.github_repo}}/issues/{{issue.number}})*

---

{{body}}

{% if issue.labels %}
## Categories

This example belongs to the following categories:

{% for label in issue.labels %} * [{{label.output_name}}]({{label.output_filename}})
{% endfor %}

{% endif %}
