import random as rnd
from src.field import Field
from src.agent_config import AgentActivity, AgentState

ID: int = 0


class Agent:
    id: int
    field: Field
    world = None
    agent_state: AgentState
    agent_activity: AgentActivity

    def __init__(self, world):
        global ID
        ID += 1
        self.id = ID
        self.world = world

    def step(self):
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)
