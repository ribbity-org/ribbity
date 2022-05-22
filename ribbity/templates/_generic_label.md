{# receives 'label, 'issues_for_label, and 'piggy' #}

# Category: {{label.output_name}}

{% for issue in issues_for_label %}
[{{config.issue_title_prefix}}{{issue.title}}]({{issue.output_filename}})
{% endfor %}
