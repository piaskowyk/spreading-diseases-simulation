from src.agent_config import AgentHealthState
from src.field import Field


class WorldSearcher:
    world = None

    @staticmethod
    def get_nearby_infectable_agents(field: Field, self_agent, r: int = 0):
        if r == 0:
            r = 1
        world = WorldSearcher.world
        output = []
        for x in range(max(0, field.x - r), min(world.width, field.x + r + 1)):
            for y in range(max(0, field.y - r), min(world.height, field.y + r + 1)):
                agent = world.fields[x][y].agent
                if agent and self_agent != agent and (agent.status is AgentHealthState.SICK or
                                                      agent.status is AgentHealthState.INFECTED):
                    output.append(agent)
        return output

    @staticmethod
    def get_nearby_health_agents(field: Field, self_agent, r: int = 0):
        if r == 0:
            r = 1
        world = WorldSearcher.world
        output = []
        for x in range(max(0, field.x - r), min(world.width, field.x + r + 1)):
            for y in range(max(0, field.y - r), min(world.height, field.y + r + 1)):
                agent = world.fields[x][y].agent
                if agent and self_agent != agent and (agent.status is AgentHealthState.HEALTHY):
                    output.append(agent)
        return output
