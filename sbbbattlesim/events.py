import collections
import logging

logger = logging.getLogger(__name__)


class SSBBSEvent:
    priority = 0
    def __init__(self, character):
        self.character = character

    def __call__(self, *args, **kwargs):
        pass


class Start(SSBBSEvent):
    '''Start of brawl'''


class Death(SSBBSEvent):
    '''A character'''


class Buff(SSBBSEvent):
    '''A character is buffed'''


class Support(SSBBSEvent):
    '''A character is supported'''


class Aura(SSBBSEvent):
    '''A character is buffed by an Aura'''


class Slay(SSBBSEvent):
    '''A slay is triggered'''


class Spawn(SSBBSEvent):
    '''A character is summoned'''


class Spell(SSBBSEvent):
    '''A spell is cast'''


class Attack(SSBBSEvent):
    '''An attacking character attacks'''


class Defend(SSBBSEvent):
    '''A defending character is attacked'''


class DamagedAndSurvived(SSBBSEvent):
    '''A character gets damaged and doesn't die'''


class EventManager:
    # TODO Make a temp register option for effects that trigger but are temporary
    # Alternaitvely figure out a good way to temporarily apply slay to something
    def __init__(self):
        self._events = collections.defaultdict(list)

    def register(self, event):
        event_base = event.__class__.__base__.__name__
        self._events[event_base].append(event)
        logger.debug(f'Registered {event_base} - {event}')

    def unregister(self, event):
        self._events.pop(event, None)

    def __call__(self, event, **kwargs):
        logger.debug(f'{self} triggered event {event}')
        for evt in sorted(self._events.get(event, ()), key=lambda x: x.priority):
            evt(**kwargs)
