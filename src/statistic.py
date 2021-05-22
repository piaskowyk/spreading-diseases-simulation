from datetime import datetime
from src.world import World


class Statistic:
    world: World
    is_collect_statistics: bool = False
    result_file = None
    data_batch: list[str] = []
    epoch: int = 0

    def __init__(self, world):
        if self.is_collect_statistics:
            self.result_file = open(datetime.now().strftime("%d-%m-%Y_%H:%M:%S.csv"), "a")
            self.result_file.write('epoch,all_agents')
            self.world = world

    def collect_statistics(self):
        if not self.is_collect_statistics:
            return

        epoch = self.epoch
        all_agents = len(self.world.agents)
        self.data_batch.append(f'{epoch},{all_agents}')
        self.epoch += 1

        if len(self.data_batch) > 100:
            self.result_file.write('\n'.join(self.data_batch))
            self.data_batch = []

