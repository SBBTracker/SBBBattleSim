import logging
import pkgutil
import traceback
from collections import OrderedDict

logger = logging.getLogger(__name__)

logic_path = __path__


class Hero:
    display_name = ''
    id = ''

    def __init__(self, player):
        self.player = player
        self.aura = None

    def pretty_print(self):
        return self.display_name


class Registry(object):
    heros = OrderedDict()

    def __getitem__(self, item):
        return self.heros.get(item, Hero)

    def __getattr__(self, item):
        return getattr(self.heros, item)

    def __contains__(self, item):
        return item in self.heros

    def register(self, name, hero):
        assert name not in self.heros
        hero.id = name
        self.heros[name] = hero
        logger.debug(f'Registered {name} - {hero}')

    def filter(self, _lambda=lambda hero_cls: True):
        return (hero_cls for id, hero_cls in self.heros.items() if _lambda(hero_cls))

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            hero = __import__(name, globals(), locals(), ['HeroType'], 1)
            self.register(name, hero.HeroType)


registry = Registry()
