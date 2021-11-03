import logging
import pkgutil
from collections import OrderedDict

from sbbbattlesim.events import EventManager

logger = logging.getLogger(__name__)

logic_path = __path__


class Treasure(EventManager):
    display_name = ''
    id = ''
    aura = False

    def buff(self, target_character):
        raise NotImplementedError(self.display_name)


class Registry(object):
    treasures = OrderedDict()

    def __getitem__(self, item):
        treasure = self.treasures.get(item)

        if treasure is None:
            class NewTreasure(Treasure):
                display_name = item

            treasure = NewTreasure

        treasure.id = item

        return treasure

    def __getattr__(self, item):
        return getattr(self.treasures, item)

    def __contains__(self, item):
        return item in self.treasures

    def register(self, name, treasure):
        assert name not in self.treasures, 'Integration is already registered.'
        treasure.display_name = name
        self.treasures[name] = treasure
        logger.debug(f'Registered {name} - {treasure}')

    def unregister(self, name):
        self.treasures.pop(name, None)

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                treasure = __import__(name, globals(), locals(), ['TreasureType'], 1)
                self.register(name, treasure.TreasureType)
            except ImportError:
                pass
            except Exception as exc:
                logger.exception('Error loading treasure: {}'.format(name))


registry = Registry()
registry.autoregister()