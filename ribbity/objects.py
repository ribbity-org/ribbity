from dataclasses import dataclass

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

