import pygame
from pygame.surface import Surface
from src.world import World
from src.agent_config import AgentStateConfig, SimulationEventType


class Graphic:
    background_surface: Surface
    agent_surface: Surface
    alpha_surface: Surface
    world: World
    width: int
    height: int
    width_size: int
    height_size: int
    agent_size: int
    clock: pygame.time.Clock

    def __init__(self, world: World, width: int, height: int):
        pygame.init()
        self.world = world
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.background_surface = pygame.Surface((width, height))
        self.agent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alpha_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.width_size = int(self.width / self.world.width)
        self.height_size = int(self.height / self.world.height)
        self.agent_size = min(self.width_size, self.height_size)

    def render_grid(self):
        color_type = 0
        for x in range(self.world.width):
            for y in range(self.world.height):
                color = (200, 200, 200) if color_type % 2 else (255, 255, 255)
                color_type += 1
                pygame.draw.rect(
                    self.background_surface,
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
        self.clock.tick(10)

    def draw_world(self):
        self.render_grid()
        self.alpha_surface.fill((0, 0, 0, 0))
        self.agent_surface.fill((0, 0, 0, 0))

        for agent in self.world.agents:
            position = (
                self.width_size * agent.field.x + (self.width_size / 2),
                self.height_size * agent.field.y + (self.height_size / 2),
            )
            pygame.draw.circle(self.agent_surface, AgentStateConfig.colors[agent.status], position, self.agent_size)
            if agent.render_event:
                if agent.event == SimulationEventType.COUGH:
                    pygame.draw.circle(self.alpha_surface, (33, 33, 33, 100), position, self.agent_size * 10)
                if agent.event == SimulationEventType.SNEEZE:
                    pygame.draw.circle(self.alpha_surface, (33, 33, 33, 100), position, self.agent_size * 20)
                agent.render_event = False

        self.screen.blit(self.background_surface, (0, 0))
        self.screen.blit(self.alpha_surface, (0, 0))
        self.screen.blit(self.agent_surface, (0, 0))
