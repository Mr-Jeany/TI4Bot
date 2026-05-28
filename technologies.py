import json

from models.technology import Technology

async def get_technology(tech_id: str = None, tech_id_short: str = None):
    techs = json.load(open("data/techs.json", encoding="utf-8"))

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