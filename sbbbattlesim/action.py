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
    ROLLED_BACK = 5


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

        self._char_buffer = set()

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

    def _apply(self, char, *args, **kwargs):
        '''
        Preforms all stat changes and represents the core of any Action
        This should never be accessed outside an Action class or subclass
        If you touch this you are touching every stat change in the simulator
        '''
        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs
        self._char_buffer.add(char)

        logger.debug(f'{char.pretty_print()} started stat change')

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

    def _clear(self, char, *args, **kwargs):
        logger.debug(f'{char.pretty_print()} started stat clear')

        if self.health != 0:
            char._damage -= min(char._damage, self.health)

        if self.attack != 0:
            char._attack -= self.attack

        logger.debug(f'{char.pretty_print()} finished stat clear')

    def execute(self):
        if self.state in (ActionState.RESOLVED, ActionState.EXECUTED, ActionState.ROLLED_BACK):
            return

        for char in self.targets:
            self._apply(char)

        self.state = ActionState.EXECUTED

    def roll_back(self):
        for char in self.targets:
            self._clear(char)

        self.state = ActionState.ROLLED_BACK

    def resolve(self):
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
    def execute(self):
        self.targets = [char for char in self.targets if not char.dead]
        super().execute()
        self.targets = [char for char in self.targets if char.dead]


class Buff(Action):
    def __init__(self, priority=0, _lambda=lambda char: True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.priority = priority
        self._lambda = _lambda

    def execute(self, character=None, *args, **kwargs):
        if character:
            if not self._lambda(character):
                return
            self._apply(character, *args, **kwargs)
        else:
            for char in self.targets:
                self._apply(char, *args, **kwargs)

        self.state = ActionState.EXECUTED

    def remove(self):
        self.targets = self._char_buffer
        self.roll_back()
        self.resolve()
        self.state = ActionState.ROLLED_BACK


class SupportBuff(Buff):
    def __init__(self, *args, **kwargs):
        super().__init__(reason=StatChangeCause.SUPPORT_BUFF, temp=True, targets=None, *args, **kwargs)


class AuraBuff(Buff):
    def __init__(self, *args, **kwargs):
        super().__init__(reason=StatChangeCause.AURA_BUFF, temp=True, targets=None, *args, **kwargs)
