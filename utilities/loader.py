from models.ability import Ability
from models.faction import Faction
from models.planet import Planet
from models.technology import Technology
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

    # TODO: Starting tech that will also work with "choose..."

    # Creating abilities
    abilities = []

    ability_list = faction_dict.pop("abilities")

    if ability_list:
        for ability in ability_list:
            abilities.append(Ability(ability["name"], ability["description"]))
    else:
        abilities = None

    # Creating faction tech
    technologies = []
    technology_list = faction_dict.pop("faction_technologies", None)

    if technology_list:
        for technology in technology_list:
            new_tech = Technology(
                id=technology["id"],
                id_short=technology["id_short"],
                color=technology["color"],
                name=technology["name"],
                description=technology["description"],
                faction_specific="muaat",
                prerequisites=technology["prerequisites"]
            )

            technologies.append(new_tech)
    else:
        technologies = None

    # Create faction specific units
    faction_specific_units = []
    fsu_list = faction_dict.pop("faction_specific_units", None)

    if not fsu_list:
        faction_specific_units = None
    else:
        for unit in fsu_list:
            upgrade = unit.pop("upgrade", None)

            if upgrade:
                upgrade_unit = Unit(id=upgrade.pop("id"),
                                     unit_type=UnitType(upgrade.pop("type")),
                                     **upgrade)
            else:
                upgrade_unit = None

            new_unit = Unit(id=unit.pop("id"),
                            unit_type=UnitType(unit.pop("type")),
                            upgrade=upgrade_unit,
                            **unit)

            faction_specific_units.append(new_unit)


    # Flagship
    flagship = Unit(id=f"{faction_id}_flagship",
                    unit_type=UnitType.FLAGSHIP,
                    **faction_dict.pop("flagship"))

    # Mech
    mech = Unit(id=f"{faction_id}_mech",
                unit_type=UnitType.MECH,
                **faction_dict.pop("mech"))

    baking_faction = Faction(
        id=faction_id,
        name=name,
        emoji=emoji,
        planets=planet_list,
        starting_units=unit_list,
        abilities=abilities,
        faction_technologies=technologies,
        faction_specific_units=faction_specific_units,

        flagship=flagship,
        mech=mech,
        **faction_dict
    )

    return baking_faction
