from src.field import Field
from src.agent import Agent


class World:
    width: int
    height: int
    fields: list[list[Field]]
    agents: list[Agent]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = []
        self.agents = []
        for x in range(width):
            line = []
            for y in range(height):
                line.append(Field(x, y))
            self.fields.append(line)

    def add_agent(self, x: int, y: int, agent: Agent):
        self.agents.append(agent)
        self.fields[x][y].take(agent)

    def field_is_free(self, x: int, y: int):
        return self.fields[x][y].is_free()

    def is_possible_move(self, x: int, y: int):
        return True \
            if -1 < x < self.width and -1 < y < self.height and self.field_is_free(x, y) \
            else False

    def move_agent(self, agent: Agent, x: int, y: int):
        field = self.fields[x][y]
        if not field.is_free():
            raise Exception(f'Field ({field.x},{field.y}) is already taken.')
        agent.field.release()
        field.take(agent)

