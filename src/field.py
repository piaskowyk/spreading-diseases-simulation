from src.agent import Agent


class Field:
    x: int
    y: int
    actor: Agent

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_free(self):
        return self.actor is None
