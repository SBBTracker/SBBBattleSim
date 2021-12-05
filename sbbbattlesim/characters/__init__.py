import logging
import pkgutil
from collections import OrderedDict
from dataclasses import dataclass

from sbbbattlesim.damage import Damage
from sbbbattlesim.events import EventManager
from sbbbattlesim.heros import Hero
from sbbbattlesim.spells import Spell
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe

logger = logging.getLogger(__name__)

logic_path = __path__


@dataclass
class StatChange:
    reason: StatChangeCause
    source: ('Character', Treasure, Hero, Spell)
    attack: int
    health: int
    damage: int
    heal: int
    temp: bool

    def __repr__(self):
        return f'{self.reason} (attack={self.attack}, health={self.health}, damage={self.damage}, heal={self.heal}, temp={self.temp})'


class Character(EventManager):
    display_name = ''
    id = ''
    aura = False
    support = False
    slay = False
    quest = False
    last_breath = False
    flying = False
    ranged = False

    # TEMPLATE STATS
    _attack = 0
    _health = 0
    _level = 0
    _tribes = set()

    def __init__(self, owner, position, attack, health, golden, tribes, cost, *args, **kwargs):
        super().__init__()
        self.owner = owner

        self.position = position
        self._base_attack = attack
        self._base_health = health
        self.golden = golden
        self.tribes = {Tribe(tribe) for tribe in tribes}
        self.cost = cost

        self._temp_attack = 0
        self._temp_health = 0
        self._damage = 0
        self.slay_counter = 0
        self.dead = False
        self.invincible = False

        self.stat_history = []

    @classmethod
    def new(cls, owner, position, golden):
        return cls(
            owner=owner,
            position=position,
            golden=golden,
            attack=cls._attack * (2 if golden else 1),
            health=cls._health * (2 if golden else 1),
            tribes=cls._tribes,
            cost=cls._level
        )

    def pretty_print(self):
        return f'''{self.display_name} pos:{self.position} gold:{self.golden} ({self.attack}/{self.health})'''

    @classmethod
    def valid(cls):
        return cls._attack != 0 or cls._health != 0 or cls._level != 0

    def buff(self, target_character, *args, **kwargs):
        raise NotImplementedError

    @property
    def slay(self):
        return bool([e for e in self.get('OnAttackAndKill') if e.slay])

    @property
    def last_breath(self):
        return bool([e for e in self.get('OnDeath') if e.last_breath])

    @property
    def attack(self):
        return max(self._base_attack + self._temp_attack, 0)

    @property
    def health(self):
        return self._base_health + self._temp_health - self._damage

    @property
    def max_health(self):
        return self._base_health + self._temp_health

    def generate_attack(self, target, reason, attacker=False):
        return Damage(
            x=self.attack,
            reason=reason,
            source=self,
            targets=[target]
        )

    def change_stats(self, reason, source, attack=0, health=0, damage=0, heal=0, temp=True, *args, **kwargs):
        stat_change = StatChange(reason=reason, source=source, attack=attack, health=health, damage=damage, heal=heal, temp=temp)
        logger.debug(f'{self.pretty_print()} stat change b/c {stat_change}')

        if attack != 0 or health != 0:
            if temp:
                self._temp_attack += attack
                self._temp_health += health
            else:
                self._base_attack += attack
                self._base_health += health

            if 'origin' in kwargs:
                del kwargs['origin']
            self('OnBuff', attack=attack, health=health, damage=damage, reason=reason, temp=temp, origin=self,  *args, **kwargs)

        if damage > 0:
            if self.invincible and reason != StatChangeCause.DAMAGE_WHILE_ATTACKING:
                self('OnDamagedAndSurvived', damage=0, *args, **kwargs)
                return
            self._damage += damage

        if heal > 0:
            if heal < self._damage:
                self._damage = self._damage - heal
            else:
                self._damage = 0

        logger.debug(f'{self.pretty_print()} finishsed stat change')
        self.stat_history.append(stat_change)

        if self.health <= 0:
            self.dead = True
            logger.debug(f'{self.pretty_print()} marked for death')
        elif damage > 0:
            self('OnDamagedAndSurvived', damage=damage, *args, **kwargs)

    def clear_temp(self):
        logger.debug(f'{self.pretty_print()} clearing temp')
        super().clear_temp()

        self._temp_attack = 0
        self._temp_health = 0
        self.invincible = False


CHARACTER_EXCLUSION = (
    'SBB_CHARACTER_CAPTAINCROC',
)


class Registry(object):
    characters = OrderedDict()

    def __getitem__(self, item):
        return self.characters.get(item, self._base_character(item))

    def __getattr__(self, item):
        return getattr(self.characters, item)

    def __contains__(self, item):
        return item in self.characters

    def register(self, name, character):
        assert name not in self.characters, name
        character.id = name
        self.characters[name] = character
        logger.debug(f'Registered {name} - {character}')

    def filter(self, _lambda=lambda char_cls: True):
        return (char_cls for id, char_cls in self.characters.items() if id not in CHARACTER_EXCLUSION and _lambda(char_cls))

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                character = __import__(name, globals(), locals(), ['CharacterType'], 1)
                self.register(name, character.CharacterType)
            except Exception as exc:
                logger.exception('Error loading characters: {}'.format(name))
                raise exc

    def _base_character(self, name):
        class TempCharacter(Character):
            display_name = name
            id = name
        return TempCharacter


registry = Registry()
