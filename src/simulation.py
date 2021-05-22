import time
from src.agent import Agent
from src.graphic import Graphic
from src.statistic import Statistic
from src.util import get_it_with_probability
from src.world import World
from src.simulation_config import SimulationConfig
import random


class Simulation:
    graphic: Graphic
    world: World
    statistic: Statistic

    def __init__(self):
        self.world = World(*SimulationConfig.word_size)
        self.graphic = Graphic(self.world, *SimulationConfig.pane_size)

        if SimulationConfig.fixed_sick_cases:
            self.world.add_agent(3, 3, Agent(self.world, True))
            self.world.add_agent(4, 4, Agent(self.world, False))
            # for i in range(SimulationConfig.population_size):
            #     if i < SimulationConfig.fixed_cases_count:
            #         self.world.add_agent_on_free(Agent(self.world, True))
            #     else:
            #         self.world.add_agent_on_free(Agent(self.world, False))
        else:
            for i in range(SimulationConfig.population_size):
                self.world.add_agent_on_free(
                    Agent(self.world,
                          get_it_with_probability(
                              SimulationConfig.create_sick_agent_probability,
                              True,
                              False
                          ))
                )
        self.statistic = Statistic(self.world)

    def run(self):
        while True:
            self.step()
            self.graphic.render()
            self.statistic.collect_statistics()
            time.sleep(SimulationConfig.interval)

    def step(self):
        random.shuffle(self.world.agents)
        for agent in self.world.agents:
            agent.step()
