from datetime import datetime

from src.agent_config import AgentHealthState, AgentActivityState
from src.world import World


class Statistic:
    world: World
    is_collect_statistics: bool = True
    result_file = None
    data_batch: list[str] = []
    epoch: int = 0
    last_agents_count: int
    agents_info_copy = {}
    last_counter = {
        'all_agents': 0,
        'health': 0,
        'sick': 0,
        'death': 0,
        'quarantine': 0,
        'infected': 0,
        'recovered': 0,
        'all_health': 0,
        'all_sick': 0,
        'all_death': 0,
        'all_quarantine': 0,
        'all_infected': 0,
        'all_recovered': 0,
    }

    def __init__(self, world):
        if self.is_collect_statistics:
            self.result_file = open('./'+datetime.now().strftime("%d-%m-%Y_%H-%M-%S.csv"), "a+")
            self.result_file.write('epoch,all_agents,health,sick,death,quarantine,infected,recovered,all_health,'
                                   'all_sick,all_death,all_quarantine,all_infected,all_recovered')
            self.world = world
            self.backup_agents_info()

    def collect_statistics(self):
        if not self.is_collect_statistics:
            return

        epoch = self.epoch
        counters = self.count_types()
        self.last_counter = counters
        self.data_batch.append(f"{epoch},{counters['all_agents']},{counters['health']},{counters['sick']},"
                               f"{counters['death']},{counters['quarantine']},{counters['infected']},"
                               f"{counters['recovered']},{counters['all_health']},{counters['all_sick']},"
                               f"{counters['all_death']},{counters['all_quarantine']},{counters['all_infected']},"
                               f"{counters['all_recovered']}")
        self.epoch += 1

        if len(self.data_batch) > 20:
            self.result_file.write('\n' + '\n'.join(self.data_batch))
            self.data_batch = []
        self.backup_agents_info()

    def count_types(self):
        health, sick, death, quarantine, infected, recovered = 0, 0, 0, 0, 0, 0
        for i in range(len(self.world.agents)):
            agent = self.world.agents[i]
            if self.agents_info_copy[agent.id]['status'] != agent.status:
                if agent.status == AgentHealthState.HEALTHY:
                    health += 1
                if agent.status == AgentHealthState.SICK:
                    sick += 1
                if agent.status == AgentHealthState.INFECTED:
                    infected += 1
                if agent.status == AgentHealthState.RECOVERED:
                    recovered += 1
            elif self.agents_info_copy[agent.id]['activity'] != self.world.agents[i].agent_activity:
                if agent.agent_activity == AgentActivityState.QUARANTINE:
                    quarantine += 1

        agents_count = len(self.world.agents)
        if self.last_counter['all_agents'] == 0:
            death = 0
        else:
            death = self.last_counter['all_agents'] - agents_count
        counters = {
            'all_agents': agents_count,
            'health': health,
            'sick': sick,
            'death': death,
            'quarantine': quarantine,
            'infected': infected,
            'recovered': recovered,

            'all_health': self.last_counter['all_health'] + health,
            'all_sick': self.last_counter['all_sick'] + sick,
            'all_death': self.last_counter['all_death'] + death,
            'all_quarantine': self.last_counter['all_quarantine'] + quarantine,
            'all_infected': self.last_counter['all_infected'] + infected,
            'all_recovered': self.last_counter['all_recovered'] + recovered,
        }
        return counters

    def backup_agents_info(self):
        self.agents_info_copy = {}
        for agent in self.world.agents:
            self.agents_info_copy[agent.id] = {
                'status': agent.status,
                'activity': agent.agent_activity
            }
