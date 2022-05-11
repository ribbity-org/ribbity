from dataclasses import dataclass
import re
import yaml


@dataclass(eq=True, frozen=True)
class Label:
    color: str
    description: str
    name: str

@dataclass(eq=True, frozen=True)
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
        return f"Example {self.number}: {self.title}"

    @property
    def config(self):
        body = self.body
        if '---' not in body:       # maybe use regexp ^---$?
            return []

        start = body.find('---')
        assert start >= 0
        end = body.find('---', start + 3)
        if end == -1:
            return []

        yaml_text = body[start:end]
        return yaml.safe_load(yaml_text)
