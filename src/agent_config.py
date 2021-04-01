from enum import Enum


class AgentState(Enum):
    HEALTHY = 1
    INFECTED = 2
    SICK = 3
    RECOVERED = 4
    DEAD = 5


class AgentActivity(Enum):
    SLEEP = 1
    WALK = 2
    STAND = 3
    TALK = 4
    NONE = 5
