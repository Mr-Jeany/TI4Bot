class CustomEmoji:
    def __init__(self, custom_emoji_id, base_emoji):
        self.custom_emoji_id = custom_emoji_id
        self.base_emoji = base_emoji
        self.id = custom_emoji_id

    def __str__(self):
        return f"<tg-emoji emoji-id='{self.custom_emoji_id}'>{self.base_emoji}</tg-emoji>"

    @property
    def rich(self):
        return f"![{self.base_emoji}](tg://emoji?id={self.custom_emoji_id})"

class UnitsEmoji:
    carrier = CustomEmoji(
        "5249050334701068122",
        "🚀"
    )

    dreadnought = CustomEmoji(
        "5249449285623258726",
        "🚀"
    )

    cruiser = CustomEmoji(
        "5246936437697321098",
        "🚀"
    )

    fighter = CustomEmoji(
        "5249158250049345965",
        "🚀"
    )

    destroyer = CustomEmoji(
        "5249191359952231178",
        "🚀"
    )

    warsun = CustomEmoji(
        "5229040764968805275",
        "🌞"
    )

    flagship = CustomEmoji(
        "5229066702276304464",
        "🚀"
    )

    infantry = CustomEmoji(
        "5249443650626164757",
        "🤖"
    )

    mech = CustomEmoji(
        "5230997083917423709",
        "🤖"
    )

    pds = CustomEmoji(
        "5247012205215389641",
        "🏠"
    )

    space_dock = CustomEmoji(
        "5246912922751377208",
        "🏠"
    )



