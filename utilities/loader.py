from models.faction import Faction
from models.planet import Planet
from models.unit import Unit, UnitType
from utilities.static_objects import StaticUnits
from utils import CustomEmoji


async def load_faction(faction_id, faction_dict) -> Faction:
    # Removing unnecessary keys and assigning them to variables
    faction_dict.pop("id")
    name = faction_dict.pop("name")

    # Creating emoji
    custom_emoji = faction_dict.pop("emoji")
    emoji = CustomEmoji(custom_emoji.pop("id"), custom_emoji.pop("base_emoji"))

    # Creating planets
    planet_list = []
    for planet in faction_dict.pop("planets"):
        planet_list.append(Planet(name=planet["name"],
                                  resource=planet["resource"],
                                  influence=planet["influence"]))

    # Creating units
    unit_list = []
    for unit in faction_dict.pop("starting_units"):
        unit_list.append(
            (unit["id"], unit["count"])
        )

    # Flagship
    flagship = Unit(id=f"{faction_id}_flagship",
                    unit_type=UnitType.FLAGSHIP,
                    **faction_dict.pop("flagship"))

    baking_faction = Faction(
        id=faction_id,
        name=name,
        emoji=emoji,
        planets=planet_list,
        starting_units=unit_list,

        flagship=flagship,
        **faction_dict
    )

    return baking_faction
