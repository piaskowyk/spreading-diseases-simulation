import random as rnd

from src.SimulationEvent import SimulationEvent
from src.agent_probability_calculator import calculate_infection_duration, calculate_death_probability, \
    calculate_sickness_duration, calculate_recovered_duration, calculate_infection_probability, \
    calculate_cough_probability, calculate_sneeze_probability
from src.field import Field
from src.agent_config import AgentActivityState, AgentHealthState, SimulationEventType
from src.util import is_with_probability
from src.world_searcher import WorldSearcher

ID: int = 0


class Agent:
    id: int
    field: Field
    world = None
    status: AgentHealthState
    agent_activity: AgentActivityState

    render_event = False
    event = 0

    infection_probability = 0
    cough_probability = 0
    sneeze_probability = 0
    current_state_cool_down = 0
    resistance = 0
    has_symptoms = None

    def __init__(self, world, is_sick):
        global ID
        ID += 1
        self.id = ID
        self.world = world
        self.status = AgentHealthState.SICK if is_sick else AgentHealthState.HEALTHY
        if self.status is AgentHealthState.SICK:
            self.current_state_cool_down = calculate_sickness_duration()
        self.infection_probability = calculate_infection_probability()
        self.cough_probability = calculate_cough_probability()
        self.sneeze_probability = calculate_sneeze_probability()

    def step(self):
        self.update_state()
        self.walk()
        self.infection_check()
        self.cough_or_sneeze()

    def walk(self):
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)

    def cough_or_sneeze(self):
        if self.status is not AgentHealthState.SICK:
            return
        if is_with_probability(self.cough_probability):
            self.render_event = True
            self.event = SimulationEventType.COUGH
        if is_with_probability(self.sneeze_probability):
            self.render_event = True
            self.event = SimulationEventType.SNEEZE
        if self.render_event:
            self.world.push_event(SimulationEvent(self.field, self.event))

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
                self.current_state_cool_down = calculate_recovered_duration()

            if self.status is AgentHealthState.INFECTED:
                self.status = AgentHealthState.SICK
                self.current_state_cool_down = calculate_sickness_duration()

        self.death_check()

    def death_check(self):
        if self.status is AgentHealthState.SICK:
            if is_with_probability(calculate_death_probability()):
                self.status = AgentHealthState.DEAD

    def infection_check(self):
        if self.status in [AgentHealthState.SICK, AgentHealthState.RECOVERED, AgentHealthState.INFECTED]:
            return
        sick_agents = WorldSearcher.get_nearby_infectable_agents(self.field, self)
        if len(sick_agents) > 0 and self.is_infection_happen():
            self.status = AgentHealthState.INFECTED
            self.current_state_cool_down = calculate_infection_duration()
