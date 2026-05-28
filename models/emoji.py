class CustomEmoji:
    def __init__(self, custom_emoji_id, base_emoji):
        self.custom_emoji_id = custom_emoji_id
        self.base_emoji = base_emoji

    def __str__(self):
        return f"<tg-emoji emoji-id='{self.custom_emoji_id}'>{self.base_emoji}</tg-emoji>"