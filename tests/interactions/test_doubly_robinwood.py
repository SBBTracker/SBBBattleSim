from sbbbattlesim import fight
from tests import make_character, make_player


def test_robinwood_doubly():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=5, attack=15, health=1),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_ROBINWOOD', attack=1, health=1),
        ],
    )
    fight(player, enemy, limit=0)

    assert (player.characters[5].attack, player.characters[5].health) == (1, 1)
