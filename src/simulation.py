import time
from src.agent import Agent
from src.graphic import Graphic
from src.world import World
import random


class Simulation:
    graphic: Graphic
    world: World

    def __init__(self):
        self.world = World(10, 10)
        self.graphic = Graphic(self.world, 400, 400)
        self.world.add_agent(0, 0, Agent(self.world))
        self.world.add_agent(2, 3, Agent(self.world))

    def run(self):
        while True:
            self.step()
            self.graphic.render()
            time.sleep(1)

    def step(self):
        random.shuffle(self.world.agents)
        for agent in self.world.agents:
            agent.step()
