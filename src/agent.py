import random as rnd

from src.simulation_event import SimulationEvent
from src.agent_probability_calculator import calculate_infection_duration, calculate_death_probability, \
    calculate_sickness_duration, calculate_recovered_duration, calculate_infection_probability, \
    calculate_cough_probability, calculate_sneeze_probability, calculate_symptoms_probability
from src.field import Field
from src.agent_config import AgentActivityState, AgentHealthState, SimulationEventType
from src.simulation_config import SimulationConfig
from src.util import is_with_probability, get_value_with_variation, rand_from_set
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
    infection_probability_factor = 0
    cough_probability = 0
    sneeze_probability = 0
    current_state_cool_down = 0
    action_duration = 0
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
        self.do_action()
        self.infection_check()
        self.do_event()

    def do_action(self):
        self.talk()
        self.walk()

    def walk(self):
        if self.agent_activity != AgentActivityState.NONE or is_with_probability(SimulationConfig.stand_probability):
            return
        x = self.field.x + rnd.randint(-1, 1)
        y = self.field.y + rnd.randint(-1, 1)
        if self.world.is_possible_move(x, y):
            self.world.move_agent(self, x, y)

    def talk(self):
        if self.agent_activity != AgentActivityState.NONE:
            return
        talkable_agents = WorldSearcher.get_nearby_talkable_agents(self.field, self)
        if len(talkable_agents) == 0 \
                or not is_with_probability(SimulationConfig.talk_probability):
            return
        self.agent_activity = AgentActivityState.TALK
        action_duration = get_value_with_variation(
            SimulationConfig.talk_duration,
            SimulationConfig.talk_duration_variation
        )
        mate = rand_from_set(talkable_agents)
        if mate.agent_activity != AgentActivityState.TALK:
            mate.agent_activity = AgentActivityState.TALK
        elif mate.action_duration < action_duration:
            action_duration = (mate.action_duration + action_duration) / 2
            mate.action_duration = action_duration
        self.action_duration = action_duration
        self.infection_probability_factor = SimulationConfig.talk_infection_probability_factor

    def do_event(self):
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
        current_infection_probability = self.infection_probability + self.infection_probability_factor
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
        if self.action_duration > 0:
            self.action_duration -= 1
        if self.action_duration <= 0:
            self.agent_activity = AgentActivityState.NONE
            self.infection_probability_factor = 0

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
            self.action_duration = SimulationConfig.quarantine_duration

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
