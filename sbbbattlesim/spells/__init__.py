import logging
import pkgutil
from collections import OrderedDict

logger = logging.getLogger(__name__)

logic_path = __path__


class Spell:
    display_name = ''
    id = ''
    _level = 0
    targeted = False
    priority = 0

    def __init__(self, player: 'Player'):
        self.player = player

    def cast(self, target: 'Character' = None, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def filter(cls, char):
        return True

    @classmethod
    def valid(cls):
        return cls._level != 0

    def pretty_print(self):
        return self.display_name


class Registry(object):
    spells = OrderedDict()
    auto_registered = False

    def __getitem__(self, item):
        return self.spells.get(item, Spell)

    def __getattr__(self, item):
        return getattr(self.spells, item)

    def __contains__(self, item):
        return item in self.spells

    def register(self, name, spell):
        assert name not in self.spells, name
        assert spell.valid(), name
        spell.id = name
        self.spells[name] = spell
        logger.debug(f'Registered {name} - {spell}')

    def filter(self, _lambda=lambda spell_cls: True):
        return (spell_cls for spell_cls in self.spells.values() if _lambda(spell_cls))

    def autoregister(self):
        if self.auto_registered:
            return
        self.auto_registered = True

        for _, name, _ in pkgutil.iter_modules(logic_path):
            spell = __import__(name, globals(), locals(), ['SpellType'], 1)
            self.register(name, spell.SpellType)


registry = Registry()
