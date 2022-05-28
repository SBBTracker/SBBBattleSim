import logging
import pkgutil
from collections import OrderedDict

from sbbbattlesim.events import EventManager

logger = logging.getLogger(__name__)

logic_path = __path__


class Treasure(EventManager):
    display_name = ''
    id = ''

    _level = 0

    def __init__(self, player, mimic):
        self.player = player

        self.mimic = mimic
        self.aura = None

    def pretty_print(self):
        return self.display_name

    def valid(self):
        return self._level != 0


class Registry(object):
    treasures = OrderedDict()
    auto_registered = False

    def __getitem__(self, item):
        return self.treasures.get(item, Treasure)

    def __getattr__(self, item):
        return getattr(self.treasures, item)

    def __contains__(self, item):
        return item in self.treasures

    def register(self, name, treasure):
        assert name not in self.treasures
        treasure.id = name
        self.treasures[name] = treasure
        logger.debug(f'Registered {name} - {treasure}')

    def filter(self, _lambda=lambda treasure_cls: True):
        return (treasure_cls for treasure_cls in self.values() if _lambda(treasure_cls))

    def autoregister(self):
        if self.auto_registered:
            return
        self.auto_registered = True

        for _, name, _ in pkgutil.iter_modules(logic_path):
            treasure = __import__(name, globals(), locals(), ['TreasureType'], 1)
            self.register(name, treasure.TreasureType)


registry = Registry()
