class Field:
    x: int
    y: int
    agent = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_free(self) -> bool:
        return False if self.agent else True

    def take(self, agent):
        self.agent = agent
        self.agent.field = self

    def release(self):
        self.agent.field = None
        self.agent = None

