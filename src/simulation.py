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
            for i in range(SimulationConfig.population_size):
                if i < SimulationConfig.fixed_cases_count:
                    self.world.add_agent_on_free(Agent(self.world, True))
                else:
                    self.world.add_agent_on_free(Agent(self.world, False))
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

    def step(self):
        random.shuffle(self.world.agents)
        self.world.clear_death_agents()
        for agent in self.world.agents:
            agent.step()
        self.world.process_step_effects()
