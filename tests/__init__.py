from sbbbattlesim import configure_logging
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart

PLAYER = {
    'characters': [],
    'treasures': [],
    'hero': '',
    'spells': [],
    'hand': [],
    'level': 0
}

CHARACTER = {
    "id": 'TEST',
    "attack": 1,
    "health": 1,
    "golden": False,
    "cost": 0,
    "position": 1,
    "keywords": [],
    "tribes": []
}


def make_player(**kwargs):
    player = PLAYER.copy()
    player.update(kwargs)
    return player


def make_character(**kwargs):
    character = CHARACTER.copy()
    character.update(kwargs)
    return character


from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart


class SpawnOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        spawn = self.source.spawn_char.new(player=self.source.player, golden=False, position=self.source.spawn_pos)
        self.source.player.summon(self.source.spawn_pos, [spawn])


class TestSpawnCharacter(Character):
    def __init__(self, spawn_char, spawn_pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spawn_char = spawn_char
        self.spawn_pos = spawn_pos
        self.player.board.register(SpawnOnStart, source=self)

from sbbbattlesim import character_registry
character_registry.register('SPAWN_TEST', TestSpawnCharacter)
