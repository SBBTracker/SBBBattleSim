import collections
import inspect
import logging
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


class SSBBSEvent:
    def __init__(self, manager, priority=0, **kwargs):
        self.manager = manager
        self.priority = priority

        for kw, arg in kwargs.items():
            setattr(self, kw, arg)

    def __call__(self, *args, **kwargs):
        # TODO Add more logging???
        return self.handle(*args, **kwargs)

    @classmethod
    def is_valid(cls):
        return True

    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


class OnSummon(SSBBSEvent):
    '''A unit is summoned'''

    def handle(self, summoned_characters, stack, *args, **kwargs):
        raise NotImplementedError


class OnStart(SSBBSEvent):
    '''Start of Brawl'''

    def handle(self, stack, *args, **kwargs):
        raise NotImplementedError


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
    slay = None

    def __call__(self, *args, **kwargs):
        response = self.handle(*args, **kwargs)

        if self.slay and not response:
            return 'OnSlay', [], {}

        return response

    def handle(self, killed_character, stack, *args, **kwargs):
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
        self._temp = collections.defaultdict(list)
        self._events = collections.defaultdict(list)

    def pretty_print(self):
        return self.__repr__()

    def register(self, event, temp=False, **kwargs):
        if not event.is_valid():
            logger.debug(f'{self.pretty_print()} can not register invalid event {event.__name__}')
            raise ValueError

        event_base = inspect.getmro(event)[1].__name__
        event = event(manager=self, **kwargs)
        (self._temp if temp else self._events)[event_base].append(event)
        logger.debug(f'{self.pretty_print()} Registered {event_base} - {event.__class__.__name__}')
        return event

    def unregister(self, event):
        event_base = inspect.getmro(event)[1].__name__
        try:
            self._temp.get(event_base, []).remove(event)
        except ValueError:
            try:
                self._events.get(event_base, []).remove(event)
            except ValueError:
                pass

    def get(self, event):
        return sorted(self._temp.get(event, []) + self._events.get(event, []),
                      key=lambda x: (x.priority, getattr(x.manager, 'position', 0)), reverse=True)

    def clear_temp(self):
        self._temp = collections.defaultdict(list)

    def __call__(self, event, stack=None, *args, **kwargs):
        logger.debug(f'{self.pretty_print()} triggered event {event}')

        handlers = self.get(event)
        if not handlers:
            return

        # If an event stack already exists use it otherwise make a new stack
        stack = stack or EventStack(self)

        with stack.open(*args, **kwargs) as executor:
            for evt in handlers:
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
            rkwargs.update({'source': source, 'stack': self.stack, **self.kwargs})
            logger.info(f'{source} reaction {react} ({rargs} {rkwargs})')
            self.manager(react, *rargs, **rkwargs)

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
