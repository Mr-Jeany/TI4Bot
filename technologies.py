import json

from utils import TechnologySpeciality


class Technology:
    def __init__(self, id: str, id_short: str, color: str, name: str, description: str, faction_specific: str | None, prerequisites: dict | None):
        self.id = id
        self.id_short = id_short
        self.color = color
        self.color_icon = getattr(TechnologySpeciality, color)

        self.faction = None
        self.is_faction = False
        if faction_specific:
            self.faction = faction_specific
            self.is_faction = True

        self.name = name
        self.description = description
        self.prerequisites = prerequisites

    @property
    def small_text(self) -> str:
        return f"{self.color_icon} {self.name}"

    @property
    def full(self) -> str:
        prereq_part = ""
        if self.prerequisites:
            for prereq_color, prereq_number in self.prerequisites.items():
                prereq_part += f"{getattr(TechnologySpeciality, prereq_color)*prereq_number}"

            prereq_part.rstrip()
        else:
            prereq_part = "нет"


        return f"""
        <b>{self.small_text}</b> {f"\n<i>{self.faction}</i>\n" if self.is_faction else ""}
{self.description}

<b>Требования:</b> {prereq_part}
"""


async def get_technology(tech_id: str = None, tech_id_short: str = None):
    techs = json.load(open("techs.json", encoding="utf-8"))

    if tech_id is None and tech_id_short is None:
        raise ValueError("No tech id provided")
    elif not (tech_id is None or tech_id_short is None):
        raise ValueError("Only one tech id can be provided")

    search_by = "id" if tech_id else "id_short"
    search_filter = tech_id if tech_id else tech_id_short

    for tech in techs["items"]:
        if tech[search_by] == search_filter:
            return Technology(**tech)

    return None