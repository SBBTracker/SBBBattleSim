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


class OnStart(SSBBSEvent):
    '''Start of Brawl'''


class OnDeath(SSBBSEvent):
    '''A character dies'''

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs) or ('OnLastBreath', [], {})

    def handle(self, dead_thing, *args, **kwargs):
        raise NotImplementedError


class OnLastBreath(SSBBSEvent):
    '''A character last a last breath'''


class OnAttack(SSBBSEvent):
    '''An attacking character attacks'''


class OnDefend(SSBBSEvent):
    '''A defending character is attacked'''


class OnDamagedAndSurvived(SSBBSEvent):
    '''A character gets damaged and doesn't die'''


class OnAttackAndKill(SSBBSEvent):
    '''A character attacks something and kills it'''

    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs) or 'OnSlay'


class OnSlay(SSBBSEvent):
    '''A character has triggered a slay'''

class OnFightStart(SSBBSEvent):
    '''A combat has begun'''


class EventManager:
    def __init__(self):
        self._temp = collections.defaultdict(list)
        self._events = collections.defaultdict(list)

    def register(self, event, temp=False):
        #event_base = event.__class__.__base__.__name__
        event_base = inspect.getmro(event)[1].__name__
        event = event(manager=self)
        if temp:
            self._temp[event_base].append(event)
        else:
            self._events[event_base].append(event)
        logger.debug(f'Registered {event_base} - {event}')

    def unregister(self, event):
        self._events.pop(event, None)

    def clear_temp(self):
        self._temp = collections.defaultdict(list)

    def __call__(self, event, *args, **kwargs):
        logger.debug(f'{self} triggered event {event}')

        reactions = []
        for evt in sorted(self._temp.get(event, []) + self._events.get(event, []), key=lambda x: x.priority):
            logger.info(evt)
            reaction = evt(**kwargs)
            if reaction:
                reactions.append(reaction)

        for (react, evt_args, evt_kwargs) in reactions:
            self(react, *evt_args, *args, **evt_kwargs, **kwargs)