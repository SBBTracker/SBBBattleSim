from sbbbattlesim import fight
from tests import make_character, make_player


def test_slog():
    player = make_player(
        raw=True,
        characters=[
            make_character(
                position=1, attack=1, health=101,
            ),
        ],
    )
    enemy = make_player(
        raw=True,
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        characters=[
            make_character(position=1, attack=1, health=100),
        ],

    )
    fight(player, enemy)

    assert player.characters[1].health == 1
