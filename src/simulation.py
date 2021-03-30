import time
from src.agent import Agent
from src.graphic import Graphic
from src.world import World


class Simulation:
    graphic: Graphic
    world: World

    def __init__(self):
        self.world = World(10, 10)
        self.graphic = Graphic(self.world, 400, 400)

    def run(self):
        while True:
            self.step()
            self.graphic.render()
            time.sleep(0.1)

    def step(self):
        pass
