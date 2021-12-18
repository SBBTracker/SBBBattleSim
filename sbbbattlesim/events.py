import collections
import inspect
import logging
import queue
import typing
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


class SSBBSEvent:
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

    @classmethod
    def is_valid(cls):
        return True

    def __call__(self, *args, **kwargs):
        # TODO Add more logging???
        return self.handle(*args, **kwargs)

    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class OnStart(SSBBSEvent):
    '''Start of Brawl'''
    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class OnSummon(SSBBSEvent):
    '''A unit is summoned'''
    def handle(self, summoned_characters, stack, *args, **kwargs):
        raise NotImplementedError


class OnDeath(SSBBSEvent):
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

    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class OnLastBreath(SSBBSEvent):
    '''A character last a last breath'''
    def handle(self, source, stack, *args, **kwargs):
        raise NotImplementedError


class OnPreAttack(SSBBSEvent):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, defend_player, stack, *args, **kwargs):
        raise NotImplementedError


class OnPostAttack(SSBBSEvent):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, stack, *args, **kwargs):
        raise NotImplementedError


class OnPreDefend(SSBBSEvent):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, defender, stack, *args, **kwargs):
        raise NotImplementedError


class OnPostDefend(SSBBSEvent):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, stack, *args, **kwargs):
        raise NotImplementedError


class OnDamagedAndSurvived(SSBBSEvent):
    '''A character gets damaged and doesn't die'''
    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class OnAttackAndKill(SSBBSEvent):
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


class OnSlay(SSBBSEvent):
    '''A character has triggered a slay'''
    def handle(self, source, stack, *args, **kwargs):
        raise NotImplementedError


class OnSpellCast(SSBBSEvent):
    '''A player cast a spell'''
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        raise NotImplementedError


class OnBuff(SSBBSEvent):
    '''Triggered when something has a stat change'''
    def handle(self, stack, attack=0, health=0, damage=0, reason='', temp=True, *args, **kwargs):
        raise NotImplementedError


class OnSupport(SSBBSEvent):
    '''Triggered when something '''
    def handle(self, buffed, support, stack, *args, **kwargs):
        raise NotImplementedError


class OnResolveBoard(SSBBSEvent):
    '''Triggers when a player attempts to resolve the board'''
    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class EventManager:
    def __init__(self):
        self._events = collections.defaultdict(queue.PriorityQueue)
        self._event_buffer = queue.PriorityQueue()
        self._removed = []

    def pretty_print(self):
        return self.__repr__()

    def register(self, event, priority=0, source=None):
        event_base = inspect.getmro(event)[1].__name__
        logger.debug(f'{self.pretty_print()} Registered {event_base} - {event.__class__.__name__}')

        if not event.is_valid():
            raise ValueError

        event = event(manager=self, source=source or self, priority=priority)
        self._events[event_base].put_nowait(event)
        return event

    def unregister(self, event):
        self._removed.append(event)

    def get(self, event):
        events_queue = self._events[event]
        priority = None

        while True:
            try:
                next_event = events_queue.get_nowait()
            except queue.Empty:
                break

            if next_event in self._removed:
                # self._removed.remove(next_event) # Maybe?
                continue

            self._event_buffer.put(next_event)

            if priority:
                if next_event.priority < priority:
                    continue

            priority = priority or next_event.priority

            yield next_event

        self._events[event] = self._event_buffer
        self._event_buffer = queue.PriorityQueue()

    def __call__(self, event, stack=None, *args, **kwargs):
        logger.debug(f'{self.pretty_print()} triggered event {event}')

        # If an event stack already exists use it otherwise make a new stack
        stack = stack or EventStack(self)

        with stack.open(*args, **kwargs) as executor:
            for evt in self.get(event):
                logger.debug(f'Firing {evt} with {args} {kwargs}')
                executor.execute(evt, *args, **kwargs)

        return stack


class EventExecutor:
    def __init__(self, stack: 'EventStack', manager: EventManager, *args, **kwargs):
        self.stack = stack
        self.manager = manager
        self.args = args
        self.kwargs = kwargs

        self._react_buffer = []

    def __enter__(self):
        logger.debug(f'Opening Executor with ({self.args} {self.kwargs})')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for (react, rargs, rkwargs, source) in self._react_buffer:
            logger.info(f'{source} reaction {react} ({rargs} {rkwargs})')
            self.manager(react, *rargs, **(rkwargs | {'source': source, 'stack': self.stack} | self.kwargs))
        logger.debug(f'Closing Executor with ({self.args} {self.kwargs})')

    def execute(self, event, *args, **kwargs):
        response = event(stack=self.stack, *args, **kwargs)
        self.stack.stack.append(event)

        if response:
            self._react_buffer.append((*response, event))


@dataclass
class EventStack:
    manager: EventManager
    stack: List[SSBBSEvent] = field(default_factory=list)

    def __repr__(self):
        return f'{self.manager.pretty_print()} - {[evt.__class__.__name__ for evt in self.stack]}'

    def __iter__(self):
        return self.stack.__iter__()

    def open(self, *args, **kwargs):
        return EventExecutor(self, self.manager, *args, **kwargs)

    def find(self, _lambda=lambda event: True):
        return (event for event in self.stack if _lambda(event))
