import logging
import pkgutil
import traceback
import typing
from collections import OrderedDict

from sbbbattlesim.action import Damage
from sbbbattlesim.events import EventManager
from sbbbattlesim.record import Record
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

logic_path = __path__


class Character(EventManager):
    display_name = ''
    id = ''
    slay = False
    last_breath = False
    support = False
    quest = False
    flying = False
    ranged = False

    # TEMPLATE STATS
    _attack = 0
    _health = 1
    _level = 0
    _tribes = set()
    _quest_counter = 0
    _quest_event = None

    deactivated = False

    def __init__(
            self,
            player: 'Player',
            position: int,
            attack: int,
            health: int,
            golden: bool,
            tribes: typing.Iterable[typing.Union[str, Tribe]],
            cost: int,
            quest_counter: int = 0,
            *args,
            **kwargs
    ):
        super().__init__()
        self.player = player

        self.position = position
        self._base_attack = attack
        self._base_health = health
        self.golden = golden
        self.tribes = {Tribe(tribe) for tribe in tribes}
        self.cost = cost
        self.quest_counter = quest_counter

        self._damage = 0
        self.slay_counter = 0
        self.dead = False
        self.invincible = False
        self.attack_multiplier = 1
        self.support_multiplier = 1

        self.support = None
        self.aura = None

        self._action_history = []

        self.has_attacked = False

    @classmethod
    def new(cls, player: 'Player', position: int, golden: bool) -> 'Character':
        return cls(
            player=player,
            position=position,
            golden=golden,
            attack=cls._attack * (2 if golden else 1),
            health=cls._health * (2 if golden else 1),
            tribes=cls._tribes,
            cost=cls._level,
            quest_counter=cls._quest_counter
        )

    def copy(self):
        new = self.__class__(
            player=self.player,
            position=self.position,
            golden=self.golden,
            attack=self._base_attack,
            health=self._base_health,
            tribes=self._tribes,
            cost=self._level,
            quest_counter=self.quest_counter
        )

        for action in self._action_history:
            action.execute(new, setup=True, from_copy=True)

        return new

    def pretty_print(self):
        return f'''{"*" if self.golden else ""}{self.display_name}{"*" if self.golden else ""} P{self.position} ({self.attack}/{self.health}) {[tribe.value for tribe in self.tribes]}'''

    @classmethod
    def valid(cls):
        return cls._attack != 0 or cls._health != 0 or cls._level != 0

    @property
    def slay(self):
        return bool([e for e in self.get('OnAttackAndKill') if e.slay])

    @property
    def last_breath(self):
        return bool([e for e in self.get('OnDeath') if e.last_breath])

    @property
    def attack(self):
        return max(self._base_attack, 0) * self.attack_multiplier

    @property
    def health(self):
        return self._base_health - self._damage

    @property
    def max_health(self):
        return max(self._base_health, 0)

    def generate_attack(
            self,
            source: ('Character', 'Hero', 'Spell', 'Treasure', 'Player'),
            target: 'Character',
            reason: 'ActionReason',
            attacking: bool = False
    ) -> Damage:
        return Damage(
            reason=reason,
            source=source,
            targets=[target],
            damage=self.attack,
        )

    def progress_quest(self, amount):
        if self not in self.player.completed_quests:
            self.quest_counter -= amount
            self.player.combat_records.append(Record(source=self, quest_progress=amount))
            if self.quest_counter <= 0:
                self.player.completed_quests.append(self)


CHARACTER_EXCLUSION = (
    'SBB_CHARACTER_CAPTAINCROC',
    'SBB_CHARACTER_FROGPRINCE',
    'SBB_CHARACTER_AWOKENPRINCESS',
    'SBB_CHARACTER_ANGRYDWARF',
    'SBB_CHARACTER_EVILWOLF',
    'SBB_CHARACTER_CERBERUS'
)


class Registry(object):
    characters = OrderedDict()
    auto_registered = False

    def __getitem__(self, item):
        return self.characters.get(item, Character)

    def __getattr__(self, item):
        return getattr(self.characters, item)

    def __contains__(self, item):
        return item in self.characters

    def register(self, name, character):
        assert name not in self.characters, name
        character.id = name
        self.characters[name] = character
        logger.debug(f'Registered {name} - {character}')

    def filter(self, _lambda: typing.Callable[[type], bool] = lambda char_cls: True):
        return (
            char_cls for id, char_cls in self.characters.items()
            if id not in CHARACTER_EXCLUSION and _lambda(char_cls)
               and char_cls._level > 1
               and not char_cls.deactivated
        )

    def autoregister(self):
        if self.auto_registered:
            return
        self.auto_registered = True

        for _, name, _ in pkgutil.iter_modules(logic_path):
            character = __import__(name, globals(), locals(), ['CharacterType'], 1)
            self.register(name, character.CharacterType)


registry = Registry()
