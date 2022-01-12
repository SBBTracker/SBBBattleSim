from sbbbattlesim import Board
from tests import make_character, make_player


def test_phoenix_tempattack():
    player = make_player(
        characters=[
            make_character(position=1, attack=7, health=1),
            make_character(id="SBB_CHARACTER_MADMADAMMIM", position=5, attack=0, health=1, golden=True),
            make_character(position=7, attack=4, health=1)
        ],
        treasures=['SBB_TREASURE_PHOENIXFEATHER', '''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1, position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    temp_attack_char = board.p1.characters[1]
    winner, loser = board.fight(limit=1)

    assert board.p1.treasures['SBB_TREASURE_PHOENIXFEATHER'][0].feather_used
    assert board.p1.characters[1] is temp_attack_char
    assert board.p1.characters[1].attack == 7
    assert board.p1.characters[1]._action_history[-1].attack == 6



