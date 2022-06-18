import logging
import pkgutil
import typing
from collections import OrderedDict

from sbbbattlesim.characters import Character
from sbbbattlesim.player import Player

logger = logging.getLogger(__name__)

logic_path = __path__


def calculate_adv_stats(player: Player):
    adv_stats = {}

    for slug, stat in registry.stats.items():
        value = stat.calculate(player)
        if value:
            adv_stats[stat.display_name] = value

    return adv_stats


class StatBase:
    display_name: str = ''

    @classmethod
    def calculate(cls, player: Player) -> int:
        raise NotImplementedError


class Registry(object):
    stats = OrderedDict()
    auto_registered = False

    def __getitem__(self, item):
        return self.stats.get(item, Character)

    def __getattr__(self, item):
        return getattr(self.stats, item)

    def __contains__(self, item):
        return item in self.stats

    def register(self, name, stat):
        assert name not in self.stats, name
        stat.id = name
        self.stats[name] = stat
        logger.debug(f'Registered {name} - {stat}')

    def autoregister(self):
        if self.auto_registered:
            return
        self.auto_registered = True

        for _, name, _ in pkgutil.iter_modules(logic_path):
            stat = __import__(name, globals(), locals(), ['StatType'], 1)
            self.register(name, stat.StatType)


registry = Registry()