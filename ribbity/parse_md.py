"""
Parse and transform markdown. Currently uses markdown-it-py to get the
paragraph level breakdown.

This handles only a subset of the full Markdown syntax. The main thing
we need to do is ignore links in verbatim fields, which works ok
for triple-back-quote but does not work for four-space-indent blocks.

We can revisit later. Promise.
"""
import re

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode


def rewrite_internal_links(body, issues_by_number, config):
    url = re.escape(f'https://github.com/{config.github_repo}/issues/')
    pattern = f"{url}(\\d+)"

    # find and rewrite all internal links:
    m = re.search(pattern, body)
    while m:
        match_num = m.groups()[0]
        match_num = int(match_num)
        match_issue = issues_by_number[match_num]
        
        link = f"[{config.issue_title_prefix}{match_issue.title}]({match_issue.output_filename})"
        body = body[:m.start()] + link + body[m.end():]
        m = re.search(pattern, body)

    return body


def make_links_clickable(body):
    # from https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
    # match links not already in a (...) markdown block, and/or links at
    # very beginning of text.
    pattern = '([^\("]|^)(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'

    def repl(m):
        # group 1 will be leading whitespace, if any
        # group 2 will be matching URL
        leading, match_url = m.groups()

        # leave leading white space in, but before link [] starts.
        link = f"{leading}[{match_url}]({match_url})"
        return link

    body = re.sub(pattern, repl, body)
    return body


def rewrite_issue_body(body, issues_by_number, config):
    #body = rewrite_internal_links(body, issues_by_number, config)
    #body = make_links_clickable(body)

    # do our own light markdown parsing...
    parser = MarkdownIt("zero")
    tokens = parser.parse(body)
    node = SyntaxTreeNode(tokens)

    # walk across just the top paragraphs
    output = []
    for x in node.children:
        for n in x.walk():
            #print('T:', n.markup, n.type, n.tag)
            if not n.children:
                content = n.content

                # only linkify etc. stuff that's not in literal
                if content.startswith("```"):
                    output.append(content)
                else:
                    content = rewrite_internal_links(content, issues_by_number, config)
                    content = make_links_clickable(content)
                    output.append(content)

    body = "\n\n".join(output)

    return body
