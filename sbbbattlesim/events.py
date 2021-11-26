import collections
import json
import logging
import inspect
from dataclasses import dataclass, field
from queue import Queue
from typing import Dict, List

logger = logging.getLogger(__name__)


class SSBBSEvent:
    priority = 0
    def __init__(self, manager):
        self.manager = manager

    def __call__(self, *args, **kwargs):
        # TODO Add more logging???
        return self.handle(*args, **kwargs)

    @classmethod
    def is_valid(cls):
        return True

    def handle(self, *args, **kwargs):
        raise NotImplementedError


class OnSummon(SSBBSEvent):
    '''A unit is summoned'''

    def handle(self, summoned_characters, *args, **kwargs):
        raise NotImplementedError


class OnStart(SSBBSEvent):
    '''Start of Brawl'''


class OnDeath(SSBBSEvent):
    '''A character dies'''
    last_breath = None

    @classmethod
    def is_valid(cls):
        return cls.last_breath is True or cls.last_breath is False

    def __call__(self, *args, **kwargs):
        response = self.handle(*args, **kwargs)

        if self.last_breath and not response:
            return 'OnLastBreath', [], {}

        return response


class OnLastBreath(SSBBSEvent):
    '''A character last a last breath'''
    def handle(self, source, stack, *args, **kwargs):
        raise NotImplementedError


class OnPreAttack(SSBBSEvent):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, defend_player, *args, **kwargs):
        raise NotImplementedError


class OnPostAttack(SSBBSEvent):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, *args, **kwargs):
        raise NotImplementedError


class OnPreDefend(SSBBSEvent):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, *args, **kwargs):
        raise NotImplementedError


class OnPostDefend(SSBBSEvent):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, *args, **kwargs):
        raise NotImplementedError


class OnDamagedAndSurvived(SSBBSEvent):
    '''A character gets damaged and doesn't die'''


class OnAttackAndKill(SSBBSEvent):
    '''A character attacks something and kills it'''
    slay = None

    def __call__(self, *args, **kwargs):
        response = self.handle(*args, **kwargs)

        if self.slay and not response:
            return 'OnSlay', [], {}

        return response

    def handle(self, killed_character, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def is_valid(cls):
        return cls.slay is True or cls.slay is False


class OnSlay(SSBBSEvent):
    '''A character has triggered a slay'''
    def handle(self, source, stack, *args, **kwargs):
        raise NotImplementedError


class OnSpellCast(SSBBSEvent):
    '''A player cast a spell'''
    def handle(self, caster, spell, target, *args, **kwargs):
        raise NotImplementedError


class OnBuff(SSBBSEvent):
    '''Triggered when something has a stat change'''
    def handle(self, attack=0, health=0, damage=0, reason='', temp=True):
        raise NotImplementedError


class OnSupport(SSBBSEvent):
    '''Triggered when something '''
    def handle(self, buffed, support, *args, **kwargs):
        raise NotImplementedError


class OnResolveBoard(SSBBSEvent):
    '''Triggers when a player attempts to resolve the board'''
    def handle(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class EventStack:
    manager: 'EventManager'
    stack: List[SSBBSEvent] = field(default_factory=list)

    _react_buffer: List[tuple] = field(default_factory=list)
    _args_buffer: list = field(default_factory=list)
    _kwargs_buffer: dict = field(default_factory=dict)

    def append(self, item):
        self.stack.append(item)

    def __getitem__(self, item):
        return self.stack[item]

    def __iter__(self):
        return self.stack.__iter__()

    def __contains__(self, item):
        return item in self.stack

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        reactions = self._react_buffer
        args = self._args_buffer
        kwargs = self._kwargs_buffer

        self._args_buffer = []
        self._kwargs_buffer = {}
        self._react_buffer = []

        for (react, rargs, rkwargs, source) in reactions:
            rkwargs.update({'source': source, **kwargs})
            logger.info(f'{source} reaction {react} ({rargs} {rkwargs})')
            self.manager(react, stack=self, *rargs, **rkwargs)

    def open(self, *args, **kwargs):
        self._args_buffer.extend(args)
        self._kwargs_buffer.update(kwargs)
        return self

    def execute(self, event, *args, **kwargs):
        response = event(stack=self, *args, **kwargs)
        self.stack.append(event)

        if response:
            self._react_buffer.append((*response, event))


class EventManager:
    def __init__(self):
        self._temp = collections.defaultdict(list)
        self._events = collections.defaultdict(list)

    def pretty_print(self):
        return self.__repr__()

    def register(self, event, temp=False):
        if not event.is_valid():
            logger.debug(f'{self.pretty_print()} can not register invalid event {event.__name__}')
            raise NotImplementedError

        event_base = inspect.getmro(event)[1].__name__
        (self._temp if temp else self._events)[event_base].append(event(manager=self))
        logger.debug(f'{self.pretty_print()} Registered {event_base} - {event.__name__}')

    def get(self, event):
        return sorted(self._temp.get(event, []) + self._events.get(event, []), key=lambda x: (x.priority, getattr(x.manager, 'position', 0)), reverse=True)

    def clear_temp(self):
        self._temp = collections.defaultdict(list)

    def __call__(self, event, stack=None, *args, **kwargs):
        logger.debug(f'{self.pretty_print()} triggered event {event}')

        # If an event stack already exists use it otherwise make a new stack
        stack = stack or EventStack(self)

        with stack.open(*args, **kwargs):
            for evt in self.get(event):
                logger.debug(f'Firing {evt} with {args} {kwargs}')
                stack.execute(evt, *args, **kwargs)
