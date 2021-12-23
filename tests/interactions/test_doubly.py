from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe

def test_raw_doubly():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=1, attack=5, health=5, tribes=[Tribe.DWARF]),
            make_character(id='SBB_CHARACTER_ANGRYDWARF', position=5, attack=5, health=5),
        ],
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    dubly = board.p1.characters[1]
    assert dubly.attack == 5
    assert dubly.health == 5
    assert dubly._temp_attack == 4
    assert dubly._temp_health == 4
