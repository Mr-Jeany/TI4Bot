from models.unit import Unit, UnitType


class StaticUnits:
    carrier = Unit(
        id="carrier",
        unit_type=UnitType.CARRIER,
        name="Транспортник I",
        description=None,
        abilities=[],
        cost=3,
        combat=9,
        number_of_attacks=1,
        move=1,
        capacity=4
    )

    carrier2 = Unit(
        id="carrier2",
        unit_type=UnitType.CARRIER,
        name="Транспортник II",
        description=None,
        abilities=[],
        cost=3,
        combat=9,
        number_of_attacks=1,
        move=2,
        capacity=6,
        prerequisites={
            "blue": 2
        }
    )