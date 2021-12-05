import logging
import pkgutil
from collections import OrderedDict

logger = logging.getLogger(__name__)

logic_path = __path__


class Spell:
    display_name = ''
    id = ''
    level = 0
    targeted = True
    priority = 0

    def cast(self, *args, **kwargs):
        raise NotImplementedError

    def filter(self, char):
        return True

    @classmethod
    def valid(cls):
        return cls._level != 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.display_name


class TargetedSpell(Spell):
    targeted = True

    def cast(self, target, *args, **kwargs):
        raise NotImplementedError


class NonTargetedSpell(Spell):
    targeted = False

    def cast(self, player, *args, **kwargs):
        raise NotImplementedError


class Registry(object):
    spells = OrderedDict()

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
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                spell = __import__(name, globals(), locals(), ['SpellType'], 1)
                self.register(name, spell.SpellType)
            except ImportError:
                pass
            except Exception as exc:
                logger.exception('Error loading spells: {}'.format(name))



registry = Registry()
