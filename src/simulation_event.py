from src.agent_config import SimulationEventType
from src.field import Field


class SimulationEvent:
    field: Field
    event_type: SimulationEventType

    def __init__(self, field: Field, event_type: SimulationEventType):
        self.field = field
        self.event_type = event_type
