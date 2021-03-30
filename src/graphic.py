import pygame
from pygame.surface import Surface
from src.world import World


class Graphic:
    surface: Surface
    world: World
    width: int
    height: int

    def __init__(self, world: World, width: int, height: int):
        pygame.init()
        self.world = world
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        self.render_grid()

    def render_grid(self):
        width_size = self.width / self.world.width
        height_size = self.height / self.world.height
        color_type = 0
        for x in range(self.world.width):
            for y in range(self.world.height):
                color = (200, 200, 200) if color_type % 2 else (255, 255, 255)
                color_type += 1
                pygame.draw.rect(
                    self.surface,
                    color,
                    pygame.Rect(x * width_size, y * height_size, width_size, height_size)
                )
            color_type += 1

    def render(self):
        self.draw_world()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

    def draw_world(self):
        # todo
        pass
