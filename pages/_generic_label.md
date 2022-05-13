# Category: {{label.output_name}}

{% for issue in issues_for_label %}
[{{issue.output_title}}]({{issue.output_filename}})
{% endfor %}
