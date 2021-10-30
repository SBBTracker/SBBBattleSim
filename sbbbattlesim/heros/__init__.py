import logging
import pkgutil
from collections import OrderedDict

from sbbbattlesim.events import EventManager
from sbbbattlesim.sbbbsobj import SBBBSObject

logger = logging.getLogger(__name__)

logic_path = __path__


class Hero(SBBBSObject):
    pass


class Registry(object):
    heros = OrderedDict()

    def __getitem__(self, item):
        hero = self.heros.get(item)

        if hero is None:
            class NewHero(Hero):
                display_name = item

            hero = NewHero

        hero.id = item

        return hero()

    def __getattr__(self, item):
        return getattr(self.heros, item)

    def __contains__(self, item):
        return item in self.heros

    def register(self, name, hero):
        assert name not in self.heros, 'Character is already registered.'
        self.heros[name] = hero
        logger.debug(f'Registered {name} - {hero}')

    def unregister(self, name):
        self.heros.pop(name, None)

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                hero = __import__(name, globals(), locals(), ['HeroType'], 1)
                self.register(name, hero.HeroType)
            except ImportError:
                pass
            except Exception as exc:
                logger.exception('Error loading heros: {}'.format(name))


registry = Registry()
registry.autoregister()