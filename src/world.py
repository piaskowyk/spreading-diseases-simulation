from src.field import Field


class World:
    width: int
    height: int
    fields: list[list[Field]]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = []
        for x in range(width):
            line = []
            for y in range(height):
                line.append(Field(x, y))
            self.fields.append(line)
