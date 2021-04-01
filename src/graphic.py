import pygame
from pygame.surface import Surface
from src.world import World
from src.agent_config import AgentStateConfig


class Graphic:
    surface: Surface
    world: World
    width: int
    height: int
    width_size: int
    height_size: int
    clock: pygame.time.Clock

    def __init__(self, world: World, width: int, height: int):
        pygame.init()
        self.world = world
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.width_size = int(self.width / self.world.width)
        self.height_size = int(self.height / self.world.height)

    def render_grid(self):
        color_type = 0
        for x in range(self.world.width):
            for y in range(self.world.height):
                color = (200, 200, 200) if color_type % 2 else (255, 255, 255)
                color_type += 1
                pygame.draw.rect(
                    self.surface,
                    color,
                    pygame.Rect(x * self.width_size, y * self.height_size, self.width_size, self.height_size)
                )
            color_type += 1

    def render(self):
        self.draw_world()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        self.clock.tick(30)

    def draw_world(self):
        self.render_grid()
        for agent in self.world.agents:
            position = (
                self.width_size * agent.field.x + (self.width_size / 2),
                self.height_size * agent.field.y + (self.height_size / 2),
            )
            pygame.draw.circle(self.surface, AgentStateConfig.colors[agent.agent_state], position, 10)
