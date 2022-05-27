import uuid

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart, Event
from sbbbattlesim.player import Player

PLAYER = {
    'characters': [],
    'treasures': [],
    'hero': '',
    'spells': [],
    'hand': [],
    'level': 0,
}

CHARACTER = {
    "id": '',
    "attack": 1,
    "health": 1,
    "golden": False,
    "cost": 0,
    "position": 1,
    "keywords": [],
    "tribes": []
}


def make_player(**kwargs):
    return Player(**(PLAYER.copy() | {'id': uuid.uuid1()} | kwargs))


def make_character(**kwargs):
    return CHARACTER.copy() | kwargs


class TestEvent(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def handle(self, stack, *args, **kwargs):
        self.triggered = True


class SpawnOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        spawn = self.source.spawn_char.new(player=self.source.player, golden=False, position=self.source.spawn_pos)
        self.source.player.summon(self.source.spawn_pos, [spawn])


class TestSpawnCharacter(Character):
    def __init__(self, spawn_char, spawn_pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spawn_char = spawn_char
        self.spawn_pos = spawn_pos
        self.player.register(SpawnOnStart, source=self)


from sbbbattlesim import character_registry
character_registry.register('SPAWN_TEST', TestSpawnCharacter)
