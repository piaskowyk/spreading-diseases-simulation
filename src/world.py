import random

from src.simulation_event import SimulationEvent
from src.agent_config import AgentHealthState
from src.field import Field
from src.agent import Agent
from src.world_searcher import WorldSearcher


class World:
    width: int
    height: int
    fields: list[list[Field]]
    agents: list[Agent]
    event_collector: list[SimulationEvent] = []

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
        WorldSearcher.world = self

    def add_agent(self, x: int, y: int, agent: Agent):
        self.agents.append(agent)
        self.fields[x][y].take(agent)

    def add_agent_on_free(self, agent: Agent):
        self.agents.append(agent)
        x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        while not self.field_is_free(x, y):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
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

    def clear_death_agents(self):
        for agent in self.agents:
            if agent.status is AgentHealthState.DEAD:
                self.agents.remove(agent)

    def push_event(self, event: SimulationEvent):
        self.event_collector.append(event)

    def process_step_effects(self):
        for event in self.event_collector:
            event.field.agent.process_event()
        self.event_collector.clear()
