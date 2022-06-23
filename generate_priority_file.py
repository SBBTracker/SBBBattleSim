import collections
import inspect
import json
import typing

from sbbbattlesim.action import ActionState, Action, ActionReason
from sbbbattlesim.events import Event
from sbbbattlesim.player import Player

from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.characters import registry as character_registry, Character
from sbbbattlesim.stats import registry as stats_registry


PRIORITY_FILE = 'event_priorities.json'


if __name__ == '__main__':

    event_dict = collections.defaultdict(dict)

    def new_event_init(self,
            manager: ('EventManager', 'Character', 'Player', 'Board'),
            source: ('Character', 'Hero', 'Spell', 'Treasure'),
            priority: int = 0,
            **kwargs
    ):
        self.manager = manager
        self.source = source
        self.priority = priority
        self.kwargs = kwargs
        event_dict[inspect.getmro(self.__class__)[1].__name__][self.__class__.__name__] = priority

    Event.__init__ = new_event_init

    def new_action_init(
            self,
            reason: ActionReason,
            source: ('Character', 'Treasure', 'Hero', 'Spell'),
            targets: (typing.List['Character'], None) = None,
            _lambda=None,
            priority: int = 0,
            multiplier: int = 1,
            attack: int = 0,
            health: int = 0,
            damage: int = 0,
            heal: int = 0,
            event: (Event, None) = None,
            _action=None,
            temp: bool = False,
            *args,
            **kwargs
    ):
        self.reason = reason
        self.source = source
        self.targets = targets or []
        self._lambda = _lambda or (lambda _: True)
        self._action = _action
        self.priority = priority
        self.multiplier = multiplier
        self.temp = temp

        self.attack = attack * self.multiplier
        self.health = health * self.multiplier
        self.damage = damage
        self.heal = heal

        self.event = event

        self.args = args
        self.kwargs = kwargs

        self.state = ActionState.CREATED
        self._char_buffer = set()
        self._killed_char_buffer = set()
        self._event_buffer = collections.defaultdict(list)

        event_dict[self.__class__.__name__][source.display_name] = priority

    Action.__init__ = new_action_init

    fake_player = Player(id='1', hero='')
    fake_opponent = Player(id='2', hero='')
    fake_player.opponent = fake_opponent
    fake_character = Character.new(fake_player, 1, True)
    fake_player.add_character(fake_character)

    for char in character_registry.filter():
        c = char.new(fake_player, -1, True)
        if c.aura:
            c.aura.execute(fake_character)

        if c.support:
            fake_player.spawn(c, 5)
            fake_player.despawn(c)

    for treasure in treasure_registry.filter():
        t = treasure(fake_player, 0)
        if t.aura:
            if isinstance(t.aura, (tuple, set)):
                for ta in t.aura:
                    ta.execute(fake_character)
            else:
                t.aura.execute(fake_character)

    for hero in hero_registry.filter():
        h = hero(player=fake_player)
        if h.aura:
            if isinstance(h.aura, (tuple, set)):
                for ha in h.aura:
                    ha.execute(fake_character)
            else:
                h.aura.execute(fake_character)

    for spell in spell_registry.filter():
        fake_player.cast_spell(spell.id)

    prioritized_events = collections.defaultdict(dict)
    for event, evts in event_dict.items():
        prioritized_events[event] = dict(sorted(evts.items(), key=lambda evt: evt[1], reverse=True))

    with open(PRIORITY_FILE, 'w+') as file:
        file.write(json.dumps(prioritized_events, indent=4))
