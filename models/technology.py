from models.emoji import TechnologySpecialityEmoji

class Technology:
    def __init__(self, id: str, id_short: str, color: str, name: str, description: str, faction_specific: str | None, prerequisites: dict | None):
        self.id = id
        self.id_short = id_short
        self.color = color
        self.color_icon = getattr(TechnologySpecialityEmoji, color)

        self.faction = None
        self.is_faction = False

        if faction_specific:
            self.faction = faction_specific
            self.is_faction = True

        self.name = name
        self.description = description
        self.prerequisites = prerequisites

    @property
    def title(self) -> str:
        return f"{self.color_icon} {self.name}"

    @property
    def full(self) -> str:
        prereq_part = ""
        if self.prerequisites:
            for prereq_color, prereq_number in self.prerequisites.items():
                prereq_part += f"{getattr(TechnologySpecialityEmoji, prereq_color)*prereq_number}"

            prereq_part.rstrip()
        else:
            prereq_part = "нет"


        return f"""
        <b>{self.title}</b> {f"\n<i>{self.faction}</i>\n" if self.is_faction else ""}
{self.description}

<b>Требования:</b> {prereq_part}
"""

    @property
    def faction_info(self) -> str:
        return f"<b>{str(self.color_icon)*self.prerequisites[self.color]} {self.name}:</b> {self.description}"