from enum import Enum


class AgentHealthState(Enum):
    HEALTHY = 1
    INFECTED = 2
    SICK = 3
    RECOVERED = 6
    DEAD = 7


class AgentStateConfig:
    colors = {
        AgentHealthState.HEALTHY: (64, 255, 64),
        AgentHealthState.INFECTED: (255, 182, 13),
        AgentHealthState.SICK: (255, 13, 41),
        AgentHealthState.RECOVERED: (41, 166, 41),
        AgentHealthState.DEAD: (0, 0, 0),
    }


class AgentActivityState(Enum):
    SLEEP = 1
    WALK = 2
    STAND = 3
    SICK = 4
    TALK = 5
    WEAR_MASK = 6
    QUARANTINE = 7
    NONE = 8


class SimulationEventType(Enum):
    NONE = 0,
    COUGH = 1,
    SNEEZE = 2
