import collections
import inspect
import logging
import queue
import typing
from dataclasses import dataclass, field
from typing import List
import copy

from sbbbattlesim.record import Record

logger = logging.getLogger(__name__)


class Event:
    def __init__(
            self,
            manager: ('EventManager', 'Character', 'Player', 'Board'),
            source: ('Character', 'Hero', 'Spell', 'Treasure'),
            priority: int = 0,
            **kwargs
    ):
        self.manager = manager
        self.source = source
        self.priority = priority
        self.kwargs = kwargs

    def __ge__(self, other):
        return self.priority >= other.priority

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return self.priority <= other.priority

    def __gt__(self, other):
        return not self.__le__(other)

    @classmethod
    def is_valid(cls):
        return True

    def __call__(self, *args, **kwargs):
        # TODO Add more logging???
        return self.handle(*args, **kwargs)

    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class OnSetup(Event):
    '''On Setup of Brawl'''


class OnStart(Event):
    '''Start of Brawl'''


class OnSpawn(Event):
    '''Triggered after a unit spawns'''


class OnDespawn(Event):
    '''Triggered after a unit despawns'''


class OnSummon(Event):
    '''A unit is summoned'''
    def handle(self, summoned_characters, stack, *args, **kwargs):
        raise NotImplementedError


class OnDeath(Event):
    '''A character dies'''
    last_breath: typing.ClassVar[bool] = False

    @classmethod
    def is_valid(cls):
        return cls.last_breath is True or cls.last_breath is False

    def __call__(self, *args, **kwargs):
        response = self.handle(*args, **kwargs)

        if self.last_breath and not response:
            return 'OnLastBreath', [], {}

        return response

    def handle(self, stack, reason, *args, **kwargs):
        raise NotImplementedError


class OnLastBreath(Event):
    '''A character last a last breath'''
    def handle(self, source, stack, *args, **kwargs):
        raise NotImplementedError


class OnPreAttack(Event):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, defend_player, stack, *args, **kwargs):
        raise NotImplementedError


class OnPostAttack(Event):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, stack, *args, **kwargs):
        raise NotImplementedError


class OnPreDefend(Event):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, defender, stack, *args, **kwargs):
        raise NotImplementedError


class OnPostDefend(Event):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, stack, *args, **kwargs):
        raise NotImplementedError


class OnDamagedAndSurvived(Event):
    '''A character gets damaged and doesn't die'''


class OnAttackAndKill(Event):
    '''A character attacks something and kills it'''
    slay: typing.ClassVar[bool] = False

    @classmethod
    def is_valid(cls):
        return cls.slay is True or cls.slay is False

    def __call__(self, *args, **kwargs):
        response = self.handle(*args, **kwargs)

        if self.slay and not response:
            return 'OnSlay', [], {}

        return response

    def handle(self, killed_character, stack, *args, **kwargs):
        raise NotImplementedError


class OnSlay(Event):
    '''A character has triggered a slay'''
    def handle(self, source, stack, *args, **kwargs):
        raise NotImplementedError


class OnSpellCast(Event):
    '''A player cast a spell'''
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        raise NotImplementedError


class OnBuff(Event):
    '''Triggered when something has a stat change'''
    def handle(self, stack, attack, health, reason=None, *args, **kwargs):
        raise NotImplementedError


class OnSupport(Event):
    '''Triggered when something '''
    def handle(self, buffed, support, stack, *args, **kwargs):
        raise NotImplementedError


class EventManager:
    def __init__(self):
        self._events = collections.defaultdict(set)

    def pretty_print(self):
        return self.__repr__()

    def register(self, event, priority=0, source=None, **kwargs):
        if not event.is_valid():
            raise ValueError

        event_base = inspect.getmro(event)[1].__name__
        event = event(manager=self, source=source or self, priority=priority, **kwargs)
        logger.debug(f'{self.pretty_print()} Registered {event_base} - {event.__class__.__name__}')
        self._events[event_base].add(event)
        return event

    def unregister(self, event):
        event_base = inspect.getmro(event.__class__)[1].__name__
        logger.debug(f'Unregistering {event} of type {event_base}')
        self._events[event_base] = self._events[event_base] - {event}

    def get(self, event):
        evts = self._events.get(event, set())
        evts_set = set(evts)
        processed_events = set()

        if not evts:
            return

        sorting_lambda = lambda x: (x.priority, getattr(x.manager, 'position', 0))
        evts = sorted(evts, key=sorting_lambda, reverse=True)

        priority = None

        while True:
            if not evts:
                break

            evt = evts[0]
            evts = evts[1:]

            processed_events.add(evt)

            if priority is None:
                priority = evt.priority
            elif evt.priority < priority:
                priority = evt.priority
            elif evt.priority > priority:
                continue

            yield evt

            new_evts_set = self._events.get(event, set())

            if evts_set != new_evts_set:
                evts_set = set(new_evts_set) - processed_events
                evts = sorted(evts_set, key=sorting_lambda, reverse=True)

            if not evts:
                break

    def __call__(self, event, stack=None, *args, **kwargs):
        logger.debug(f'{self.pretty_print()} triggered event {event}')

        # If an event stack already exists use it otherwise make a new stack
        stack = stack or EventStack()

        if not self._events[event]:
            return stack

        with stack.open(*args, **kwargs) as executor:
            for evt in self.get(event):
                logger.debug(f'Firing {evt} with {args} {kwargs}')
                executor.execute(evt, *args, **kwargs)

        return stack


class EventExecutor:
    def __init__(self, stack: 'EventStack', *args, **kwargs):
        self.stack = stack
        self.args = args
        self.kwargs = kwargs

        self._react_buffer = []

    def __enter__(self):
        # logger.info(f'Opening Executor with ({self.args} {self.kwargs})')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for (react, rargs, rkwargs, source) in reversed(self._react_buffer):
            logger.info(f'{source} reaction {react} ({rargs} {rkwargs})')
            source.manager(react, *rargs, **(rkwargs | {'source': source, 'stack': self.stack} | self.kwargs))

    def execute(self, event, *args, **kwargs):
        response = event(stack=self.stack, *args, **kwargs)
        self.stack.stack.append(event)

        if response:
            self._react_buffer.append((*response, event))


@dataclass
class EventStack:
    stack: List[Event] = field(default_factory=list)

    def __repr__(self):
        return f'{[evt.__class__.__name__ for evt in self.stack]}'

    def __iter__(self):
        return self.stack.__iter__()

    def open(self, *args, **kwargs):
        return EventExecutor(stack=self, *args, **kwargs)

    def find(self, _lambda=lambda event: True):
        return (event for event in self.stack if _lambda(event))
