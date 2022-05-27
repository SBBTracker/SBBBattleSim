import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('level', (2, 3, 4, 5, 6))
@pytest.mark.parametrize('repeat', range(30))
def test_donkey_surviving(golden, level, repeat):
    player = make_player(
        raw=True,
        level=level,
        characters=[
            make_character(id='SBB_CHARACTER_TROJANDONKEY', attack=1, health=3, position=1, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)

    assert player.characters[2] is not None
    if golden:
        assert player.characters[2]._level == level
    else:
        assert player.characters[2]._level <= level and player.characters[2]._level > 1


def test_donkey_fullboard():
    player = make_player(
        raw=True,
        level=6,
        characters=[
            make_character(id='SBB_CHARACTER_TROJANDONKEY', attack=1, health=3, position=7),
            make_character(id='', attack=1, health=3, position=2),
            make_character(id='', attack=1, health=3, position=3),
            make_character(id='', attack=1, health=3, position=4),
            make_character(id='', attack=1, health=3, position=5),
            make_character(id='', attack=1, health=3, position=6),
            make_character(id='', attack=1, health=1, position=1),
        ],
        treasures=['SBB_TREASURE_REDUPLICATOR', 'SBB_TREASURE_TREASURECHEST']
    )
    enemy = make_player(
        spells=['SBB_SPELL_FALLINGSTARS']
    )

    fight(player, enemy, limit=1)
