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

    def is_valid(self):
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

    def is_valid(self):
        return self.last_breath is True or self.last_breath is False

    def __call__(self, *args, **kwargs):
        response = self.handle(*args, **kwargs)

        if self.last_breath and not response:
            return 'OnLastBreath', [], {}

        return response


class OnLastBreath(SSBBSEvent):
    '''A character last a last breath'''
    def handle(self, source, *args, **kwargs):
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

    def is_valid(self):
        return self.slay is True or self.slay is False


class OnSlay(SSBBSEvent):
    '''A character has triggered a slay'''
    def handle(self, source, *args, **kwargs):
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


class EventManager:
    def __init__(self):
        self._temp = collections.defaultdict(list)
        self._events = collections.defaultdict(list)

    def pretty_print(self):
        return self.__repr__()

    def register(self, event, temp=False):
        event_base = inspect.getmro(event)[1].__name__
        event = event(manager=self)

        if not event.is_valid():
            logger.debug(f'{self.pretty_print()} found invalid event {event_base} - {event.__class__.__name__}')
            raise NotImplementedError

        if temp:
            self._temp[event_base].append(event)
        else:
            self._events[event_base].append(event)
        logger.debug(f'{self.pretty_print()} Registered {event_base} - {event.__class__.__name__}')

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

    def get(self, event):
        return sorted(self._temp.get(event, []) + self._events.get(event, []), key=lambda x: (x.priority, getattr(x.manager, 'position', 0)), reverse=True)

    def clear_temp(self):
        self._temp = collections.defaultdict(list)

    def __call__(self, event, *args, **kwargs):
        # This is so hugely sensitive with regards to changes to Baba Yaga
        # if you can't update baba yaga while updating this code then you shouldn't change either
        logger.debug(f'{self.pretty_print()} triggered event {event}')
        reactions = []
        for evt in self.get(event):
            logger.debug(f'Firing {evt} with {args} {kwargs}')
            reaction = evt(*args, **kwargs)
            if reaction:
                reactions.append((*reaction, evt))

        for (react, evt_args, evt_kwargs, source) in reactions:
            # evt_args += args
            evt_kwargs.update({'source': source, **kwargs})
            logger.info(f'{react} reacting to {event} with source={source} ({evt_args} {evt_kwargs})')
            self(react, *evt_args, **evt_kwargs)

    def event_type_is_registered(self, type):
        """
        Does not check for specific events like polywoggle slay
        instead checks for thigns like OnBuff
        """
        if not isinstance(type, str):
            type = inspect.getmro(type)[1].__name__

        return type in self._temp or type in self._events