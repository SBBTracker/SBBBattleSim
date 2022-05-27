import pytest

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
from tests import make_character, make_player


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_puffpuff_spawn(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=1, attack=7, health=7),
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


    assert (player.characters[1].attack, player.characters[1].health) == (2, 2)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_puffpuff_spawn_high_health(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=1, attack=7, health=70000),
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


    assert (player.characters[1].attack, player.characters[1].health) == (2, 2)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_puffpuff_spawn_high_attack(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=1, attack=70000, health=7),
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


    assert (player.characters[1].attack, player.characters[1].health) == (2, 2)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_puffpuff_spawn_with_large(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=1, attack=50, health=50),
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=5, attack=50, health=50),
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=6, attack=50, health=50),
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


    assert (player.characters[5].attack, player.characters[5].health) == (51, 51)
    assert (player.characters[1].attack, player.characters[1].health) == (45, 45)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_puffpuff_spawn_with_large_golden(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=1, attack=1000, health=1000),
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=5, attack=50, health=50, golden=True),
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


    assert (player.characters[1].attack, player.characters[1].health) == (20, 20)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('raw', (True, False))
def test_puffpuff_spawn_with_large_and_echowood(r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=1, attack=50, health=50),
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=5, attack=50, health=50),
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=6, attack=50, health=50),
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


    assert (player.characters[1].attack, player.characters[1].health) == (45, 45)
    assert (player.characters[5].attack, player.characters[5].health) == (51, 51)
    assert (player.characters[7].attack, player.characters[7].health) == (47, 47)


@pytest.mark.parametrize('r', range(5))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('raw', (True, False))
def test_puff_spawn(golden, r, raw):
    player = make_player(
        raw=raw,
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", position=7, attack=17, health=17),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=1, attack=1, health=1),
        ]
    )
    enemy = make_player(
        spells=["SBB_SPELL_LIGHTNINGBOLT"]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_PUFFPUFF"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=golden
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[7].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=2)


    assert (player.characters[6].attack, player.characters[6].health) == (34, 34) if golden else (17, 17), (player.characters[6].attack, player.characters[6].health)
    assert (player.characters[1].attack, player.characters[1].health) == (21, 21) if golden else (11, 11), (player.characters[1].attack, player.characters[1].health)
