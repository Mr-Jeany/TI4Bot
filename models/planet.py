class Planet:
    name: str
    resource: int
    influence: int

    def __init__(self, name: str, resource: int, influence: int):
        self.name = name
        self.resource = resource
        self.influence = influence