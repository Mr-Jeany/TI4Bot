import asyncio

from models.ability import Ability
from models.faction import Faction
from models.leader import Leader, LeaderTypes
from models.planet import Planet
from models.promissory_note import PromissoryNote
from models.technology import Technology
from models.unit import Unit, UnitType
from utils import CustomEmoji

async def load_all_factions(faction_json_converted: dict) -> dict[str, Faction]:
    async def load_one(item: dict):
        faction_id = item["id"]
        faction = await asyncio.to_thread(load_faction, faction_id, item)
        return faction_id, faction

    results = await asyncio.gather(
        *(load_one(item) for item in faction_json_converted["items"])
    )

    return dict(results)

def load_faction(faction_id, faction_dict) -> Faction:
    # Removing unnecessary keys and assigning them to variables
    faction_dict.pop("id")
    name = faction_dict.pop("name")

    commodities = faction_dict.pop("commodities")
    complexity = faction_dict.pop("complexity")

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

    # Starting tech
    # TODO: Make it work with "choose a tech..."
    # TODO: Make it with objects
    starting_technologies = faction_dict.pop("starting_technologies")
    tech_list = []

    for tech in starting_technologies:
        tech_list.append((tech["name"], tech["color"]))

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

    # PN
    pn = faction_dict.pop("promissory_note")

    prom_note = PromissoryNote(
        id=f"{faction_id}_pn",
        name=pn["name"],
        description=pn["description"],
    )

    # Agent
    agent_d = faction_dict.pop("agent")
    agent = Leader(id=f"{faction_id}_agent",
                   type=LeaderTypes.AGENT,
                   name=agent_d["name"],
                   description=agent_d["description"]
                   )

    # Commander
    commander_d = faction_dict.pop("commander")
    commander = Leader(id=f"{faction_id}_commander",
                   type=LeaderTypes.COMMANDER,
                   name=commander_d["name"],
                   description=commander_d["description"],
                   unlocking=commander_d["condition"]
                   )

    # Hero
    hero_d = faction_dict.pop("hero")
    hero = Leader(id=f"{faction_id}_hero",
                   type=LeaderTypes.HERO,
                   name=hero_d["name"],
                   description=hero_d["description"],
                   unlocking="Имейте 3 выполненные цели."
                   )


    baking_faction = Faction(
        id=faction_id,
        name=name,

        commodities=commodities,
        complexity=complexity,

        emoji=emoji,
        planets=planet_list,
        starting_units=unit_list,
        abilities=abilities,
        faction_technologies=technologies,
        faction_specific_units=faction_specific_units,
        promissory_note=prom_note,
        agent=agent,
        commander=commander,
        hero=hero,

        flagship=flagship,
        mech=mech,

        starting_technologies=tech_list,
    )

    return baking_faction
