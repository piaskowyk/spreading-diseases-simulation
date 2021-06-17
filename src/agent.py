import random as rnd

from src.simulation_event import SimulationEvent
from src.agent_probability_calculator import calculate_infection_duration, calculate_death_probability, \
    calculate_sickness_duration, calculate_recovered_duration, calculate_infection_probability, \
    calculate_cough_probability, calculate_sneeze_probability, calculate_symptoms_probability
from src.field import Field
from src.agent_config import AgentActivityState, AgentHealthState, SimulationEventType
from src.simulation_config import SimulationConfig
from src.util import is_with_probability
from src.world_searcher import WorldSearcher

ID: int = 0


class Agent:
    id: int
    field: Field
    world = None
    status: AgentHealthState
    agent_activity: AgentActivityState = AgentActivityState.NONE

    render_event = False
    event = SimulationEventType.NONE

    infection_probability = 0
    cough_probability = 0
    sneeze_probability = 0
    current_state_cool_down = 0
    quarantine_cool_down = 0
    resistance = 0
    has_symptoms = False
    wearing_mask = False

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
        self.has_symptoms = is_with_probability(calculate_symptoms_probability())
        self.wearing_mask = is_with_probability(SimulationConfig.wearing_mask_probability)

    def step(self):
        self.update_state()
        self.walk()
        self.infection_check()
        self.cough_or_sneeze()

    def walk(self):
        if self.agent_activity == AgentActivityState.QUARANTINE:
            return
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)

    def cough_or_sneeze(self):
        if self.status is not AgentHealthState.SICK or not self.has_symptoms:
            return
        if is_with_probability(self.cough_probability):
            self.render_event = True
            self.event = SimulationEventType.COUGH
        if is_with_probability(self.sneeze_probability):
            self.render_event = True
            self.event = SimulationEventType.SNEEZE
        if self.render_event:
            self.world.push_event(SimulationEvent(self.field, self.event))

    def is_infection_happen(self, sick_agents, is_from_symptom=False):
        if len(sick_agents) == 0:
            return False
        all_wear_mask = True
        for agent in sick_agents:
            if not agent.wearing_mask:
                all_wear_mask = False
                break
        current_infection_probability = self.infection_probability
        protection = 0
        if all_wear_mask:
            protection = SimulationConfig.wearing_mask_other_protection_factor
        if self.wearing_mask:
            protection = SimulationConfig.wearing_mask_self_protection_factor
        if is_from_symptom:
            current_infection_probability += SimulationConfig.symptom_infection_factor
            protection *= SimulationConfig.symptom_protection_factor
        current_infection_probability = current_infection_probability - protection

        if current_infection_probability < 0:
            current_infection_probability = 0
        if current_infection_probability > 1:
            current_infection_probability = 1
        if self.status is AgentHealthState.SICK:
            return False
        return is_with_probability(current_infection_probability)

    def update_state(self):
        if self.quarantine_cool_down > 0:
            self.quarantine_cool_down -= 1
        if self.quarantine_cool_down == 0 and self.agent_activity == AgentActivityState.QUARANTINE:
            self.agent_activity = AgentActivityState.NONE

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
                self.quarantine_check()

        self.death_check()

    def death_check(self):
        if self.status is AgentHealthState.SICK:
            if is_with_probability(calculate_death_probability()):
                self.status = AgentHealthState.DEAD

    def quarantine_check(self):
        if is_with_probability(SimulationConfig.quarantine_probability):
            self.agent_activity = AgentActivityState.QUARANTINE
            self.quarantine_cool_down = SimulationConfig.quarantine_duration

    def infection_check(self):
        if self.status in [AgentHealthState.SICK, AgentHealthState.RECOVERED, AgentHealthState.INFECTED]:
            return
        sick_agents = WorldSearcher.get_nearby_infectable_agents(self.field, self)
        if self.is_infection_happen(sick_agents):
            self.status = AgentHealthState.INFECTED
            self.current_state_cool_down = calculate_infection_duration()

    def process_event(self):
        if self.event is SimulationEventType.COUGH:
            self.symptom_action(SimulationConfig.cough_radius)
        if self.event is SimulationEventType.SNEEZE:
            self.symptom_action(SimulationConfig.sneeze_radius)

    def symptom_action(self, r: int):
        health_agents = WorldSearcher.get_nearby_health_agents(self.field, self, r)
        for agent in health_agents:
            agent.infection_check_after_event(self)

    def infection_check_after_event(self, source_agent):
        if self.is_infection_happen([source_agent], True):
            self.status = AgentHealthState.INFECTED
            self.current_state_cool_down = calculate_infection_duration()
