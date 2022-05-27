from sbbbattlesim import fight
from tests import make_character, make_player


def test_bouncy_cupid():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_CUPID", position=5, attack=1, health=5),
            make_character(id="SBB_CHARACTER_CUPID", position=1, attack=1, health=5),
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id="SBB_CHARACTER_CUPID", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=1)

    assert player.characters[1].health == 1
    assert player.characters[5] is None
