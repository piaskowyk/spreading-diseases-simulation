import random as rnd
from src.field import Field
from src.agent_config import AgentActivityState, AgentHealthState
from src.simulation_config import SimulationConfig
from src.util import is_with_probability, get_value_with_variation
from src.world_searcher import WorldSearcher

ID: int = 0


class Agent:
    id: int
    field: Field
    world = None
    agent_state: AgentHealthState
    agent_activity: AgentActivityState

    infection_probability = 0
    current_state_cool_down = 0
    resistance = 0

    def __init__(self, world, is_sick):
        global ID
        ID += 1
        self.id = ID
        self.world = world
        self.agent_state = AgentHealthState.SICK if is_sick else AgentHealthState.HEALTHY
        if self.agent_state is AgentHealthState.SICK:
            self.current_state_cool_down = self.calculate_sickness_cool_down()
        self.infection_probability = self.calculate_infection_probability()

    def step(self):
        self.update_state()
        self.walk()
        if self.agent_state != AgentHealthState.SICK:
            sick_agents = WorldSearcher.get_nearby_sick_agents(self.field, self)
            if len(sick_agents) > 0 and self.is_infection_happen():
                self.agent_state = AgentHealthState.SICK
                self.current_state_cool_down = self.calculate_sickness_cool_down()

    def walk(self):
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)

    def sleep_action(self):
        pass

    def is_infection_happen(self):
        if self.agent_state is AgentHealthState.SICK:
            return False
        return is_with_probability(self.infection_probability)

    def update_state(self):
        if self.current_state_cool_down == 0:
            return
        self.current_state_cool_down -= 1
        if self.current_state_cool_down == 0:
            if self.agent_state is AgentHealthState.SICK:
                self.agent_state = AgentHealthState.HEALTHY
        self.death_check()


    def calculate_sickness_cool_down(self):
        return get_value_with_variation(
            SimulationConfig.sickness_cool_down,
            SimulationConfig.sickness_cool_down_variation
        )

    def calculate_infection_probability(self):
        return get_value_with_variation(
            SimulationConfig.infection_probability,
            SimulationConfig.infection_probability_variation
        )

    def calculate_resistance(self):
        return get_value_with_variation(
            SimulationConfig.agent_resistance,
            SimulationConfig.agent_resistance_variation
        )

    def death_check(self):
        if self.agent_state is not AgentHealthState.SICK:
            return
        if is_with_probability(SimulationConfig.death_probability):
            self.agent_state = AgentHealthState.DEAD
