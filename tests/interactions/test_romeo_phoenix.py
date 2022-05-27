import pytest

from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_phoenix_makes_romeo_sad(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=6, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            'SBB_TREASURE_PHOENIXFEATHER'
        ]
    )
    enemy = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_LIGHTNINGDRAGON",
                attack=7,
                health=8
            )
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = player.characters[2]
    winner, loser = board.fight(limit=2)


    assert player.characters[6] is None
    assert not juliet.dead
