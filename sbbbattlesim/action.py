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


class Action:
    def __init__(
            self,
            reason: StatChangeCause,
            source: ('Character', Treasure, Hero, Spell),
            targets: List['Character'],
            attack: int = 0,
            health: int = 0,
            damage: int = 0,
            heal: int = 0,
            temp: bool = False,
            *args,
            **kwargs
    ):
        self.reason = reason
        self.source = source
        self.targets = targets

        self.attack = attack
        self.health = health
        self.damage = damage
        self.heal = heal
        self.temp = temp

        self.args = args
        self.kwargs = kwargs

        self._active = False

        self.state = ActionState.CREATED

        logger.debug(f'New {self}')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        prefix = f'{self.source} {self.reason} {self.targets}'

        stats = ''
        if self.attack > 0 or self.health > 0:
            stats = f'+{self.attack}/{self.health}'
        elif self.attack < 0 or self.health < 0:
            stats = f'-{self.attack}/{self.health}'
        elif self.damage != 0:
            stats = f'!{self.damage}'
        elif self.health != 0:
            stats = f'~{self.heal}'

        args = f'({self.args} {self.kwargs})'

        return f'{prefix} {stats} {args}'

    def __enter__(self):
        self._active = True
        self.execute()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        self.resolve()

    def _(self, char, *args, **kwargs):
        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs
        if self.attack != 0 or self.health != 0:

            if self.temp:
                char._temp_attack += self.attack
                char._temp_health += self.health
            else:
                char._base_attack += self.attack
                char._base_health += self.health

            # TRIGGER ON BUFF
            char('OnBuff', reason=self.reason, source=self.source,
                 attack=self.attack, health=self.health, damage=self.damage, temp=self.temp,
                 *args, **kwargs)

        if self.damage > 0:
            if char.invincible and self.reason != StatChangeCause.DAMAGE_WHILE_ATTACKING:
                char('OnDamagedAndSurvived', damage=0, *args, **kwargs)
                return
            char._damage += self.damage

        if self.heal != 0:
            char._damage = 0 if self.heal == -1 else max(char._damage - self.heal, 0)

        logger.debug(f'{char.pretty_print()} finishsed stat change')
        char._action_history.append(self)

        if char.health <= 0:
            char.dead = True
            logger.debug(f'{char.pretty_print()} marked for death')
        elif self.damage > 0:
            char('OnDamagedAndSurvived', damage=self.damage, *args, **kwargs)

    def execute(self):
        if self.state in (ActionState.RESOLVED, ActionState.EXECUTED):
            return

        for char in self.targets:
            self._(char)

        self.state = ActionState.EXECUTED

    def resolve(self):
        if self.state == ActionState.CREATED:
            self.execute()
        elif self.state == ActionState.RESOLVED:
            logger.debug(f'{self} ALREADY RESOLVED')
            return

        dead_characters = []

        logger.debug(f'RESOLVING DAMAGE FOR {self}')

        for char in self.targets:
            if char in char.player.graveyard:
                logger.debug(f'{char.pretty_print()} already in graveyard')
                continue

            if char.dead:
                dead_characters.append(char)
                char.player.graveyard.append(char)
                char.player.characters[char.position] = None
                logger.info(f'{char.pretty_print()} died')

        logger.info(f'These are the dead characters: {dead_characters}')
        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath')

        self.state = ActionState.RESOLVED


class Damage(Action):
    def execute(self):
        self.targets = [char for char in self.targets if not char.dead]
        super().execute()
        self.targets = [char for char in self.targets if char.dead]


class Buff(Action):
    pass


class SupportBuff(Buff):
    def __init__(
            self,
            priority=0,
            reason=StatChangeCause.SUPPORT_BUFF,
            temp=True,
            _lambda=lambda char: True,
            *args,
            **kwargs
    ):
        super().__init__(reason=reason, temp=temp, targets=None, *args, **kwargs)
        self.priority = priority
        self._lambda = _lambda

    def execute(self, character, *args, **kwargs):
        if not self._lambda(character):
            return

        self._(character, *args, **kwargs)


class AuraBuff(Buff):

    def __init__(
            self,
            priority=0,
            reason=StatChangeCause.AURA_BUFF,
            temp=True,
            _lambda=lambda char: True,
            *args,
            **kwargs
    ):
        super().__init__(reason=reason, temp=temp, targets=None, *args, **kwargs)
        self.priority = priority
        self._lambda = _lambda

    def execute(self, character, *args, **kwargs):
        if not self._lambda(character):
            return

        self._(character, *args, **kwargs)

