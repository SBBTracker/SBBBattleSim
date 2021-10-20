import pkgutil
import logging
from collections import OrderedDict


logger = logging.getLogger(__name__)

logic_path = __path__


class Treasure:
    name = ''


class Registry(object):
    treasures = OrderedDict()

    def __getitem__(self, item):
        return self.treasures.get(item, lambda: None)()

    def __getattr__(self, item):
        return getattr(self.treasures, item)

    def __contains__(self, item):
        return item in self.treasures

    def register(self, name, integration):
        assert name not in self.treasures, 'Integration is already registered.'
        integration.name = name
        self.treasures[name] = integration

    def unregister(self, name):
        self.treasures.pop(name, None)

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                treasure = __import__(name, globals(), locals(), ['PingPost'], 1)
                if self.is_valid(name, treasure):
                    self.register(name, treasure.PingPost)
            except ImportError:
                pass
            except Exception as exc:
                logger.exception('Error loading treasure: {}'.format(name))


registry = Registry()