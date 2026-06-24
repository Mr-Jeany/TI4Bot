from dataclasses import dataclass
from enum import Enum

from PIL import Image

from models.planet import Planet

class TileType(str, Enum):
    RED = "red" # no planets
    BLUE = "blue" # with planet(s)
    NOTHING = "nothing" # pretty much anything else (hyperlanes and mecatol)

@dataclass
class Tile:
    id: int
    planets: list[Planet]
    is_home_system: int
    tile_type: TileType
    is_anomaly: bool = False
    extra: list[str] | None = None
    image: Image.Image | None = None

    contains_legendary: bool = False

    def __post_init__(self):
        self.contains_legendary = any(
            planet.is_legendary for planet in self.planets
        )


    @property
    def optimal(self) -> tuple[int, int]:
        if not self.planets:
            return 0, 0

        resource = 0
        influence = 0
        for planet in self.planets:
            resource += planet.resource
            influence += planet.influence

        return resource, influence