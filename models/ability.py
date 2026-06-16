class Ability:
    name: str
    description: str

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"<b>{self.name}:</b> {self.description}"