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
    status: AgentHealthState
    agent_activity: AgentActivityState

    infection_probability = 0
    current_state_cool_down = 0
    resistance = 0

    def __init__(self, world, is_sick):
        global ID
        ID += 1
        self.id = ID
        self.world = world
        self.status = AgentHealthState.SICK if is_sick else AgentHealthState.HEALTHY
        if self.status is AgentHealthState.SICK:
            self.current_state_cool_down = self.calculate_sickness_duration()
        self.infection_probability = self.calculate_infection_probability()

    def step(self):
        self.update_state()
        self.walk()
        self.infection_check()

    def walk(self):
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)

    def cough(self):
        pass

    def is_infection_happen(self):
        if self.status is AgentHealthState.SICK:
            return False
        return is_with_probability(self.infection_probability)

    def update_state(self):
        if self.current_state_cool_down == 0:
            return
        self.current_state_cool_down -= 1
        if self.current_state_cool_down == 0:
            if self.status is AgentHealthState.RECOVERED:
                self.status = AgentHealthState.HEALTHY

            if self.status is AgentHealthState.SICK:
                self.status = AgentHealthState.RECOVERED
                self.current_state_cool_down = self.calculate_recovered_duration()

            if self.status is AgentHealthState.INFECTED:
                self.status = AgentHealthState.SICK
                self.current_state_cool_down = self.calculate_sickness_duration()

        self.death_check()

    def death_check(self):
        if self.status is AgentHealthState.SICK:
            if is_with_probability(self.calculate_death_probability()):
                self.status = AgentHealthState.DEAD

    def infection_check(self):
        if self.status is AgentHealthState.SICK or self.status is AgentHealthState.RECOVERED:
            return
        sick_agents = WorldSearcher.get_nearby_infectable_agents(self.field, self)
        if len(sick_agents) > 0 and self.is_infection_happen():
            self.status = AgentHealthState.INFECTED
            self.current_state_cool_down = self.calculate_infection_duration()

    def calculate_sickness_duration(self):
        return get_value_with_variation(
            SimulationConfig.sickness_duration,
            SimulationConfig.sickness_duration_variation
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

    def calculate_infection_duration(self):
        return get_value_with_variation(
            SimulationConfig.infection_duration,
            SimulationConfig.infection_duration_variation
        )

    def calculate_recovered_duration(self):
        return get_value_with_variation(
            SimulationConfig.recovered_duration,
            SimulationConfig.recovered_duration_variation
        )

    def calculate_death_probability(self):
        return get_value_with_variation(
            SimulationConfig.death_probability,
            SimulationConfig.death_probability_variation
        )

    def calculate_cough_probability(self):
        return get_value_with_variation(
            SimulationConfig.cough_probability,
            SimulationConfig.cough_probability_variation
        )
