import collections
import inspect
import json

from sbbbattlesim.events import Event
from sbbbattlesim.player import Player

from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.stats import registry as stats_registry


PRIORITY_FILE = 'event_priorities.json'


if __name__ == '__main__':

    event_dict = collections.defaultdict(dict)

    def new_init(
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

        event_dict[inspect.getmro(self.__class__)[1].__name__][self.__class__.__name__] = self.priority

    Event.__init__ = new_init

    fake_player = Player(id='g', hero='')

    for char in character_registry.filter():
        char.new(fake_player, -1, True)

    for treasure in treasure_registry.filter():
        treasure(fake_player, 0)

    for hero in hero_registry.filter():
        hero(player=fake_player)

    for spell in spell_registry.filter():
        spell(fake_player)

    prioritized_events = collections.defaultdict(dict)
    for event, evts in event_dict.items():
        prioritized_events[event] = dict(sorted(evts.items(), key=lambda evt: evt[1], reverse=True))

    with open(PRIORITY_FILE, 'w+') as file:
        file.write(json.dumps(prioritized_events, indent=4))