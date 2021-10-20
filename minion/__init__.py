import logging
import pkgutil
from collections import OrderedDict
from copy import copy

logger = logging.getLogger(__name__)

logic_path = __path__


class Minion:
    name = 'NO NAME SET'

    slay = []
    buffs = []
    death = []
    on_damage = []

    def __init__(self, attack, health, position=None, *tribes):
        self.attack_bonus = 0
        self.health_bonus = 0
        self.base_attack = attack
        self.base_health = health
        self._damage = 0
        self.slay_counter = 0
        self.position = position

        self.tribes = tribes

        self.slay_funcs = []
        self.buff_funcs = []
        self.death_funcs = []
        self.damage_funcs = []

        self.owner = None

        for slay in self.slay:
            self.slay_funcs.append(slay(self))

        for death in self.death:
            self.death_funcs.append(death(self))

        for damage_func in self.on_damage:
            self.damage_funcs.append(damage_func(self))

        self.buffs = [buff(self) for buff in self.buffs]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.name} ({self.attack}/{self.health})'

    def damage_event(self, value, **kwargs):
        self._damage += value

        if self._damage > self.health:
            del self
            return True

        for damage_func in self.damage_funcs:
            damage_func(damage_target=self, **kwargs)

        return False

    def slay_event(self, slayed, **kwargs):
        for slay in self.slay_funcs:
            slay(slayed=slayed, **kwargs)


    @property
    def attack(self):
        return self.base_attack + self.attack_bonus

    @property
    def health(self):
        return self.base_health + self.health_bonus - self.damage


class Registry(object):
    minions = OrderedDict()

    def __getitem__(self, item):
        minion = self.minions.get(item)
        if not minion:
            class NewMinion(Minion):
                name = item
            minion = NewMinion
            # print(f'Creating Generic Minion for {item}')
        return minion

    def __getattr__(self, item):
        return getattr(self.minions, item)

    def __contains__(self, item):
        return item in self.minions

    def register(self, name, minion):
        assert name not in self.minions, 'Minion is already registered.'
        self.minions[name] = minion
        print(f'Registered {name} - {minion}')

    def unregister(self, name):
        self.minions.pop(name, None)

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                minion = __import__(name, globals(), locals(), ['PingPost'], 1)
                self.register(name, minion.MinionType)
            except ImportError:
                pass
            except Exception as exc:
                logger.exception('Error loading minion: {}'.format(name))


registry = Registry()