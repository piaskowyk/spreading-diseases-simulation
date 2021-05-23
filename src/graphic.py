import pygame
from pygame.surface import Surface
from src.world import World
from src.agent_config import AgentStateConfig, Effect


class Graphic:
    background_surface: Surface
    agent_surface: Surface
    alpha_surface: Surface
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
        self.screen = pygame.display.set_mode((width, height))
        self.background_surface = pygame.Surface((width, height))
        self.agent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alpha_surface = pygame.Surface((width, height), pygame.SRCALPHA)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("click")
                if event.button == 4:
                    print("scrollTop")
                if event.button == 5:
                    print("scrollDown")
            if event.type == pygame.MOUSEMOTION:
                print(pygame.mouse.get_pos())
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
            pygame.draw.circle(self.agent_surface, AgentStateConfig.colors[agent.status], position, 10)
            if agent.render_effect:
                if agent.effect == Effect.COUGH:
                    pygame.draw.circle(self.alpha_surface, (33, 33, 33, 100), position, 100)
                if agent.effect == Effect.SNEEZE:
                    pygame.draw.circle(self.alpha_surface, (33, 33, 33, 100), position, 200)
                agent.render_effect = False

        self.screen.blit(self.background_surface, (0, 0))
        self.screen.blit(self.alpha_surface, (0, 0))
        self.screen.blit(self.agent_surface, (0, 0))
