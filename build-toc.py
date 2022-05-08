#! /usr/bin/env python
import sys
import argparse
import pprint
import re
import os
import time
import glob
import yaml
from collections import OrderedDict


mkdocs_yml = """\
site_name: My Docs

nav:
{nav}
"""

def main():
    p = argparse.ArgumentParser()
    args = p.parse_args()

    all_files = glob.glob('docs/?-*.md')
    all_files = [ x[5:] for x in all_files ] # remove docs/ prefix

    sort_key = lambda x: int(x.split('-')[0])
    all_files.sort(key=sort_key)

    all_pages = []
    for n, filename in enumerate(all_files):
        with open(f"docs/{filename}", "rt") as fp:
            title = fp.readline()
            title = title[2:].strip()

        d = {}
        d[title] = filename
        all_pages.append(d)

    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append(dict(Examples=all_pages))
    
    print(mkdocs_yml.format(nav=yaml.safe_dump(nav_contents)))

    with open('docs/examples.md', 'wt') as fp:
        fp.write("# All examples")
        for filename in all_files:
            with open(f"docs/{filename}", "rt") as fp2:
                title = fp2.readline()
                title = title[2:].strip()
            fp.write(f"""

[{title}]({filename})
            
""")

    return 0


if __name__ == '__main__':
    sys.exit(main())
