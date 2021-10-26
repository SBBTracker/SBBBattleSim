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
    def __init__(self):
        self._temp = collections.defaultdict(list)
        self._events = collections.defaultdict(list)

    def register(self, event, temp=False):
        event_base = event.__class__.__base__.__name__
        if temp:
            self._temp[event_base].append(event)
        else:
            self._events[event_base].append(event)
        logger.debug(f'Registered {event_base} - {event}')

    def unregister(self, event):
        self._events.pop(event, None)

    def clear_temp(self):
        self._temp = collections.defaultdict(list)

    def __call__(self, event, **kwargs):
        logger.debug(f'{self} triggered event {event}')
        for evt in sorted(self._temp.get(event, []) + self._events.get(event, []), key=lambda x: x.priority):
            evt(**kwargs)
