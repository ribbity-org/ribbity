from dataclasses import dataclass
import re

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
