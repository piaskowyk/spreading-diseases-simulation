import random as rnd
import src.constants as constants
from src.field import Field
from src.agent_config import AgentActivity, AgentState

ID: int = 0


class Agent:
    id: int
    field: Field
    world = None
    agent_state: AgentState
    agent_activity: AgentActivity
    steps_to_change_state: int = 0
    steps_to_change_activity: int = 0

    def __init__(self, world):
        global ID
        ID += 1
        self.id = ID
        self.world = world
        self.agent_state = AgentState.SICK if rnd.random() <= 0.01 else AgentState.HEALTHY
        self.agent_activity = AgentActivity.SICK if self.agent_state == AgentState.SICK else AgentActivity.NONE

    def step(self):
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)
        self.steps_to_change_state -= 1
        self.steps_to_change_activity -= 1
        self.change_state()
        self.change_activity()
        self.perform_activity()

    def perform_activity(self):
        if self.agent_activity == AgentActivity.SICK:
            self.cough()

    def change_state(self):
        if self.steps_to_change_state > 0:
            return
        if self.agent_state == AgentState.INFECTED:
            self.agent_state = AgentState.SICK

    def change_activity(self):
        if self.steps_to_change_activity > 0:
            return
        if self.agent_state == AgentState.SICK:
            if rnd.random() <= constants.SICK_PROBABILITY:
                self.agent_activity = AgentActivity.SICK
                self.steps_to_change_activity = constants.SICK_DURATION
            else:
                self.agent_activity = AgentActivity.NONE

    def cough(self):
        if self.agent_activity == AgentActivity.SICK:
            agents = self.world.get_agents_in_range(self.field.x, self.field.y, constants.COUGH_RANGE)
            for agent in agents:
                agent.try_to_infect(constants.COUGH_INFECTION_PROBABILITY)

    def try_to_infect(self, infection_probability: float):
        if self.agent_state == AgentState.INFECTED or self.agent_state == AgentState.SICK:
            return
        if self.agent_state == AgentState.RECOVERED:
            infection_probability /= constants.RECOVERED_RESISTANCE_RATIO
        if rnd.random() <= infection_probability:
            self.agent_state = AgentState.INFECTED
            self.steps_to_change_state = constants.INFECTION_DURATION

