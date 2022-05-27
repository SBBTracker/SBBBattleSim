import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


def test_darkwood_ranged():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_DARKWOODCREEPER", position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_FOXTAILARCHER", position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=-1)

    assert player.characters[1].attack == 1


@pytest.mark.parametrize('golden', (True, False))
def test_darkwood_melee(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_DARKWOODCREEPER", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=100),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)

    final_attack = 3 if golden else 2
    assert player.characters[1].attack == final_attack


def test_darkwood_soltak_defending():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_DARKWOODCREEPER", position=1, attack=1, health=1),
            make_character(id="SBB_CHARACTER_SOLTAKANCIENT", position=2, attack=0, health=20),
            make_character(position=5, attack=1, health=1),
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id="SBB_CHARACTER_BABYDRAGON", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=1)

    assert player.characters[5].attack == 2
