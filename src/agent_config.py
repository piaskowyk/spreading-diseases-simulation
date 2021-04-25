from enum import Enum


class AgentState(Enum):
    HEALTHY = 1
    INFECTED = 2
    SICK = 3
    RECOVERED = 4
    DEAD = 5


class AgentStateConfig:
    colors = {
        AgentState.HEALTHY: (64, 255, 64),
        AgentState.INFECTED: (255, 182, 13),
        AgentState.SICK: (255, 13, 41),
        AgentState.RECOVERED: (41, 166, 41),
        AgentState.DEAD: (0, 0, 0),
    }


class AgentActivity(Enum):
    SLEEP = 1
    WALK = 2
    STAND = 3
    SICK = 4
    TALK = 5
    NONE = 6

