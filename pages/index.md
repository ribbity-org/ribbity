# Welcome to the sourmash examples site!

This is a collection of examples and recipes for [the sourmash
software](https://sourmash.readthedocs.io/), for fast genomic and
metagenomic sequencing data analysis.

sourmash can quickly search genomes and metagenomes for matches; see
[our list of available search
databases](https://sourmash.readthedocs.io/en/latest/databases.html).

sourmash also supports taxonomic exploration and classification
for genomes and metagenomes with the NCBI and
[GTDB](https://gtdb.ecogenomic.org/) taxonomies.

The paper [Large-scale sequence comparisons with sourmash (Pierce et
al., 2019)](https://f1000research.com/articles/8-1006) gives an
overview of what sourmash does and how sourmash works.

Do you have questions or comments? [File an
issue](https://github.com/sourmash-bio/sourmash/issues) or [come chat
on gitter](https://gitter.im/sourmash-bio/community)!

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

