from sbbbattlesim import Board
from sbbbattlesim.action import ActionReason
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe


def test_burning_tree():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BURNINGTREE', position=1, attack=5, health=20, tribes=[Tribe.EVIL, Tribe.TREANT]),
            make_character(id='SBB_CHARACTER_KINGTREE', position=2, attack=0, health=20,
                           tribes=[Tribe.EVIL, Tribe.TREANT])
        ],
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)

    burning_tree = board.p1.characters[1]

    assert burning_tree.attack == 25
    assert burning_tree.health == 40


def test_burning_tree_echowoood():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BURNINGTREE', position=1, attack=5, health=20, tribes=[Tribe.EVIL, Tribe.TREANT]),
            make_character(id='SBB_CHARACTER_KINGTREE', position=2, attack=0, health=20,
                           tribes=[Tribe.EVIL, Tribe.TREANT]),
            make_character(id='SBB_CHARACTER_ECHOWOODSHAMBLER', position=7, attack=10, health=10)
        ],
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)

    burning_tree = board.p1.characters[1]
    echowood = board.p1.characters[7]

    assert burning_tree.attack == 25
    assert burning_tree.health == 40
    assert echowood.attack == 50
    assert echowood.health == 30

