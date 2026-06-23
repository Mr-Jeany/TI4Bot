from dataclasses import dataclass
from enum import Enum


class Techskip(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"

@dataclass
class Planet:
    name: str
    resource: int
    influence: int
    is_home_system: bool = False
    is_legendary: bool = False
    techskip: Techskip | None = None


    def __str__(self):
        return f"{self.name} ({self.resource}/{self.influence})"


    @property
    def optimal(self):
        if self.resource > self.influence:
            return self.resource, 0

        elif self.resource < self.influence:
            return 0, self.influence

        else:
            return self.resource, self.influence