import sys
from dataclasses import dataclass
import re
from functools import total_ordering
import tomli


DEFAULT_ISSUE_PRIORITY=999


@dataclass(eq=True, frozen=True)
class Label:
    color: str
    description: str
    name: str

    @property
    def output_name(self):
        return self.description or self.name

    @property
    def output_filename(self):
        return f"l-{self.name}.md"

@dataclass(eq=True, frozen=True)
@total_ordering
class Issue:
    number: int
    title: str
    body: str
    labels: list

    @property
    def output_filename(self):
        "A unique filename that is filesystem-pleasant: special char removed."
        title = re.sub('[^A-Za-z0-9. ]+', '', self.title)
        title = title.replace(' ', '-')
        title = title.lower()
        filename = f"{self.number}-{title}.md"
        return filename

    @property
    def output_title(self):
        "A title with prefix 'Example: '"
        return f"Example: {self.title}"

    @property
    def index_title(self):
        "A title suitable for indexes - no special characters/formatting"
        title = re.sub('[^A-Za-z0-9._ ]+', '', self.title)
        return f"Example: {title}"

    @property
    def config(self):
        body = self.body
        if '---' not in body:       # maybe use regexp ^---$?
            return {}

        start = body.find('---')
        assert start >= 0
        start += 3
        end = body.find('---', start)
        if end == -1:
            return {}

        config_text = body[start:end]
        try:
            x = tomli.loads(config_text)
        except tomli.TOMLDecodeError:
            print(f"ERROR parsing TOML from issue {self.number}.",
                  file=sys.stderr)
            print(f"TOML string: '''\n{config_text}\n'''")
            raise

        if x:
            return dict(x)
        return {}

    @property
    def is_frontpage(self):
        return self.config.get('frontpage', False)

    @property
    def is_ignored(self):
        return self.config.get('ignore', False)

    @property
    def priority(self):
        return self.config.get('priority', DEFAULT_ISSUE_PRIORITY)

    def __lt__(self, other):
        return (self.priority, self.title.lower()) < \
                (other.priority, other.title.lower())
