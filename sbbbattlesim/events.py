import collections
import logging
import inspect

logger = logging.getLogger(__name__)


class SSBBSEvent:
    priority = 0
    def __init__(self, manager):
        self.manager = manager

    def __call__(self, *args, **kwargs):
        # TODO Add more logging???
        return self.handle(*args, **kwargs)

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

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs) or ('OnLastBreath', args, kwargs)


class OnLastBreath(SSBBSEvent):
    '''A character last a last breath'''


class OnAttack(SSBBSEvent):
    '''An attacking character attacks'''
    def handle(self, attack_position, defend_position, *args, **kwargs):
        raise NotImplementedError

class OnDefend(SSBBSEvent):
    '''A defending character is attacked'''
    def handle(self, attack_position, defend_position, *args, **kwargs):
        raise NotImplementedError

class OnDamagedAndSurvived(SSBBSEvent):
    '''A character gets damaged and doesn't die'''


class OnAttackAndKill(SSBBSEvent):
    '''A character attacks something and kills it'''

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs) or ('OnSlay', args, kwargs)

    def handle(self, killed_character, *args, **kwargs):
        raise NotImplementedError


class OnSlay(SSBBSEvent):
    '''A character has triggered a slay'''

class OnFightStart(SSBBSEvent):
    '''A combat has begun'''


class OnBuff(SSBBSEvent):
    '''Triggered when something has a stat change'''
    def handle(self, attack=0, health=0, damage=0, reason='', temp=True):
        raise NotImplementedError


class EventManager:
    def __init__(self):
        self._temp = collections.defaultdict(list)
        self._events = collections.defaultdict(list)

    def register(self, event, temp=False):
        event_base = inspect.getmro(event)[1].__name__
        event = event(manager=self)
        if temp:
            self._temp[event_base].append(event)
        else:
            self._events[event_base].append(event)
        logger.debug(f'{self} Registered {event_base} - {event.__class__.__name__}')

    def unregister(self, event):
        logger.debug(f'UNREGISTERING {event} {type(event)}')
        if isinstance(event, str):
            evt_check = lambda evt: evt.__class__.__name__ == event
        elif isinstance(event, SSBBSEvent):
            evt_check = lambda evt: evt == event
        elif issubclass(event, SSBBSEvent):
            evt_check = lambda evt: evt.__class__ == event
        else:
            return

        for event_base, evts in self._events.items():
            [evts.remove(evt) for evt in evts if evt_check(evt)]
        for event_base, evts in self._temp.items():
            [evts.remove(evt) for evt in evts if evt_check(evt)]

    def clear_temp(self):
        self._temp = collections.defaultdict(list)

    def __call__(self, event, *args, **kwargs):
        logger.debug(f'{self} triggered event {event}')
        reactions = []
        for evt in sorted(self._temp.get(event, []) + self._events.get(event, []), key=lambda x: (x.priority, getattr(x.manager, 'position', 0)), reverse=True):
            logger.debug(f'Firing {evt} with {args} and {kwargs}')
            reaction = evt(*args, **kwargs)
            if reaction:
                reactions.append(reaction)

        for (react, evt_args, evt_kwargs) in reactions:
            logger.info(f'Reaction to {event} {reaction}')
            self(react, *evt_args, *args, **evt_kwargs, **kwargs)

    def event_type_is_registered(self, type):
        """
        Does not check for specific events like polywoggle slay
        instead checks for thigns like OnBuff
        """
        if not isinstance(type, str):
            type = inspect.getmro(type)[1].__name__

        return type in self._temp or type in self._events