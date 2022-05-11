from dataclasses import dataclass
import re
import yaml
from functools import total_ordering


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
        title = re.sub('[^A-Za-z0-9. ]+', '', self.title)
        title = title.replace(' ', '-')
        filename = f"{self.number}-{title}.md"
        return filename

    @property
    def output_title(self):
        return f"Example: {self.title}"

    @property
    def index_title(self):
        title = re.sub('[^A-Za-z0-9._ ]+', '', self.title)
        return f"Example: {title}"

    @property
    def config(self):
        body = self.body
        if '---' not in body:       # maybe use regexp ^---$?
            return {}

        start = body.find('---')
        assert start >= 0
        end = body.find('---', start + 3)
        if end == -1:
            return {}

        yaml_text = body[start:end]
        x = yaml.safe_load(yaml_text)
        if x:
            return dict(x)
        return {}

    @property
    def priority(self):
        return self.config.get('priority', DEFAULT_ISSUE_PRIORITY)

    def __lt__(self, other):
        return (self.priority, self.title.lower()) < \
                (other.priority, other.title.lower())
