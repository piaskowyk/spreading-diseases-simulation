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
        agent.field = self.fields[x][y]
        self.fields[x][y].free = False
