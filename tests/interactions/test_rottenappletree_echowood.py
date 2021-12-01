from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe

def test_echowood_rottenappletree():
    player = make_player(
        hero = "SBB_HERO_MUERTE",
        characters=[
            make_character(position=2, attack=1, health=100),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ROTTENAPPLETREE", health=2)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 1)
