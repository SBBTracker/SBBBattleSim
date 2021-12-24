import collections
import logging
from enum import Enum
from typing import List

from sbbbattlesim.heros import Hero
from sbbbattlesim.spells import Spell
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class ActionState(Enum):
    CREATED = 1
    EXECUTED = 2
    RESOLVED = 3
    ROLLED_BACK = 4


class Action:
    def __init__(
            self,
            reason: StatChangeCause,
            source: ('Character', Treasure, Hero, Spell),
            targets: (List['Character'], None) = None,
            _lambda=None,
            priority: int = 0,
            attack: int = 0,
            health: int = 0,
            damage: (int, None) = None,
            heal: int = 0,
            temp: bool = False,
            *args,
            **kwargs
    ):
        self.reason = reason
        self.source = source
        self.targets = targets or []
        self._lambda = _lambda or (lambda _: True)
        self.priority = priority

        self.attack = attack
        self.health = health
        self.damage = damage
        self.heal = heal
        self.temp = temp

        self.args = args
        self.kwargs = kwargs

        self.state = ActionState.CREATED
        self._char_buffer = set()

        logger.debug(f'New {self}')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.reason} {self.source.pretty_print()} >>> {[char.pretty_print() for char in self.targets]} ({self.args}, {self.kwargs})'

    def _apply(self, char, *args, **kwargs):
        '''
        This is the core of any Action class and should not be touched unless you are making changes to ALL effects
        This should never be accessed outside an Action class or subclass
        '''
        logger.debug(f'{char.pretty_print()} has {char._temp_health} temp health and {char._temp_attack} temporary attack')

        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs
        self._char_buffer.add(char)
        char._action_history.append(self)

        if self.attack != 0 or self.health != 0:
            if self.temp:
                char._temp_attack += self.attack
                char._temp_health += self.health
            else:
                char._base_attack += self.attack
                char._base_health += self.health

            # TRIGGER ON BUFF
            char('OnBuff', reason=self.reason, source=self.source,
                 attack=self.attack, health=self.health, damage=self.damage or 0, temp=self.temp,
                 *args, **kwargs)

        if self.damage not in  [0, None]:
            if char.invincible and self.reason != StatChangeCause.DAMAGE_WHILE_ATTACKING:
                char('OnDamagedAndSurvived', damage=0, *args, **kwargs)
                return
            char._damage += self.damage or 0

        if self.heal != 0:
            char._damage = 0 if self.heal == -1 else max(char._damage - self.heal, 0)

        if char.health <= 0 and self.damage is not None:
            char.dead = True
            logger.debug(f'{char.pretty_print()} marked for death')
        elif self.damage is not None and self.damage > 0:
            char('OnDamagedAndSurvived', damage=self.damage, *args, **kwargs)

    def _clear(self, char, *args, **kwargs):
        '''
        This is the core function to specify how to reverse an action and should not be touched unless you are making changes to ALL effects
        This should never be accessed outside an Action class or subclass
        '''
        if self.health != 0:
            char._damage -= min(char._damage, self.health)

        if self.attack != 0:
            char._attack -= self.attack


    def execute(self, character=None, *args, **kwargs):
        logger.debug(f'Executing {self} for character {character}')
        if self.state in (ActionState.RESOLVED, ActionState.ROLLED_BACK):
            return

        if character:
            if not self._lambda(character):
                return
            self._apply(character, *args, **kwargs)
        else:
            for char in self.targets:
                self._apply(char, *args, **kwargs)

        self.state = ActionState.EXECUTED

    def roll_back(self):
        for char in self.targets or self._char_buffer:
            self._clear(char)

        self.state = ActionState.ROLLED_BACK

    def resolve(self):
        logger.debug('Resolving for character {character}')
        if self.state == ActionState.CREATED:
            self.execute()
        elif self.state in (ActionState.RESOLVED, ActionState.ROLLED_BACK):
            logger.debug(f'{self} ALREADY RESOLVED')
            return

        logger.debug(f'RESOLVING DAMAGE FOR {self}')

        characters = self._char_buffer
        self._char_buffer = set()

        dead_characters = []

        for char in characters:
            if char in char.player.graveyard:
                logger.debug(f'{char.pretty_print()} already in graveyard')
                continue

            if char.dead:
                dead_characters.append(char)
                char.player.despawn(char)

        logger.info(f'These are the dead characters: {dead_characters}')
        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath')

        self.state = ActionState.RESOLVED


class Damage(Action):
    pass


class Heal(Action):
    pass


class Buff(Action):
    pass


class SupportBuff(Buff):
    def __init__(self, *args, **kwargs):
        super().__init__(reason=StatChangeCause.SUPPORT_BUFF, temp=True, *args, **kwargs)


class AuraBuff(Buff):
    def __init__(self, *args, **kwargs):
        super().__init__(reason=StatChangeCause.AURA_BUFF, temp=True, *args, **kwargs)


class EventAction(Action):
    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        self._event_buffer = collections.defaultdict(list)

    def _apply(self, char, *args, **kwargs):
        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs
        self._char_buffer.add(char)

        registered = char.register(self.event, temp=self.temp, *args, **kwargs)
        self._event_buffer[char].append(registered)

    def _clear(self, char, *args, **kwargs):
        for registered in self._event_buffer.get(char):
            char.unregister(registered)


class EventSupport(EventAction):
    def __init__(self, *args, **kwargs):
        super().__init__(reason=StatChangeCause.SUPPORT_BUFF, temp=True, *args, **kwargs)


class EventAura(EventAction):
    def __init__(self, *args, **kwargs):
        super().__init__(reason=StatChangeCause.AURA_BUFF, temp=True, *args, **kwargs)
