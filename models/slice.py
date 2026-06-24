from PIL import Image, ImageDraw

from models.tile import Tile


class Slice:
    """
    A class for Milty draft slices
    """

    # Indexes:
    # 1-3 - first row above home system, home system is 0
    # 4-5 - start of the next row
    tiles: list[Tile | None]


    def generate_image(self) -> Image.Image:
        images = [t.image if t is not None else None for t in self.tiles]
        width, height = images[1].size
        center_width = int(width / 4 * 3)

        coordinates = {
            0: (center_width, 2*height),
            1: (0, int(height * 1.5)),
            2: (center_width, height),
            3: (int(width * 1.5), int(height * 1.5)),
            4: (0, int(height * 0.5)),
            5: (center_width, 0),
        }

        base = Image.new(
            "RGBA",
            (int(width * 2.5), height * 3)
        )

        for index in range(len(images)):
            if images[index] is None:
                continue
            base.alpha_composite(images[index], coordinates[index])

        return base