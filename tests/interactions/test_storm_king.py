import pytest

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived, OnStart
from tests import make_character, make_player


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=2, health=2),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=7, health=7),
        ],
    )

    fight(player, enemy, limit=1)

    assert (player.characters[1].attack, player.characters[1].health) == (1, 1)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn_with_spell(r, golden, raw):
    s = 4 if golden else 2
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=s, health=s, golden=golden),
        ],
        spells=[
            'SBB_SPELL_FIREBALL'
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=100, health=700),
        ],
    )

    class CastFireballOnStart(OnStart):
        def handle(self, stack, *args, **kwargs):
            self.source.cast_spell('SBB_SPELL_FIREBALL')

    player.register(CastFireballOnStart)
    fight(player, enemy, limit=1)

    assert (player.characters[1].attack, player.characters[1].health) == (3, 3)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_cast_spell(r, golden, raw):
    s = 4 if golden else 2
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=s, health=s, golden=golden),
        ],
    )
    enemy = make_player()

    class CastFireballOnStart(OnStart):
        def handle(self, stack, *args, **kwargs):
            self.source.cast_spell('SBB_SPELL_FIREBALL')

    player.register(CastFireballOnStart)

    fight(player, enemy, limit=0)

    assert (player.characters[1].attack, player.characters[1].health) == ((8, 8) if golden else (4, 4))


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('raw', (True, False))
def test_many_stormking_cast_spell(r, golden, raw):
    s = 4 if golden else 2
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=s, health=s, golden=golden),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=2, attack=s, health=s, golden=golden),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=3, attack=s, health=s, golden=golden),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=4, attack=s, health=s, golden=golden),

        ],
    )
    enemy = make_player()

    class CastFireballOnStart(OnStart):
        def handle(self, stack, *args, **kwargs):
            self.source.cast_spell('SBB_SPELL_FIREBALL')

    player.register(CastFireballOnStart)

    fight(player, enemy, limit=0)

    for pos in [1, 2, 3, 4]:
        assert (player.characters[pos].attack, player.characters[pos].health) == ((8, 8) if golden else (4, 4))


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_storm_king_spawn_high_health(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=8, health=70000),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=7000000, health=7),
        ],
    )

    fight(player, enemy, limit=1)

    assert (player.characters[1].attack, player.characters[1].health) == (7, 7)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn_high_attack(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=70000, health=8),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=8, health=7),
        ],
    )

    fight(player, enemy, limit=1)

    assert (player.characters[1].attack, player.characters[1].health) == (7, 7)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn_with_large(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=52, health=52),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=5, attack=52, health=52),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=6, attack=52, health=52),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=52, health=52),
        ],
    )

    fight(player, enemy, limit=1)

    assert (player.characters[5].attack, player.characters[5].health) == (52, 52)
    assert (player.characters[1].attack, player.characters[1].health) == (51, 51)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn_with_large_golden(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=1000, health=1000),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=5, attack=52, health=52, golden=True),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=1000, health=1000),
        ],
    )

    fight(player, enemy, limit=1)

    assert (player.characters[1].attack, player.characters[1].health) == (25, 25)

@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn_with_large_and_echowood(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=1, attack=50, health=50),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=5, attack=50, health=50),
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=6, attack=50, health=50),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=50, health=50),
        ],
    )

    fight(player, enemy, limit=1)

    assert (player.characters[1].attack, player.characters[1].health) == (49, 49)
    assert (player.characters[5].attack, player.characters[5].health) == (50, 50)
    assert (player.characters[7].attack, player.characters[7].health) == (49, 49)

@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('raw', (True, False))
def test_stormking_spawn(golden, r, raw):

    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", position=7, attack=18, health=18),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=1, attack=1, health=1),
        ]
    )
    enemy = make_player(
        spells=["SBB_SPELL_LIGHTNINGBOLT"]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_THEGREATANDPOWERFUL"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=golden
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[7].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=2)

    assert (player.characters[6].attack, player.characters[6].health) == (36, 36) if golden else (18, 18), player.characters[6].pretty_print()
    assert (player.characters[1].attack, player.characters[1].health) == (33, 33) if golden else (17, 17), player.characters[1].pretty_print()