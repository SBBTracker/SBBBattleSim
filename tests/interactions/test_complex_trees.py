from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_complex_trees():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_GOODANDEVILSISTERS", position=1, attack=4, health=4, golden=True),
            make_character(position=2, attack=30, health=52, golden=True,
                           tribes=[Tribe.GOOD, Tribe.PRINCE, Tribe.TREANT]),
            make_character(position=3, attack=28, health=75, golden=True,
                           tribes=[Tribe.GOOD, Tribe.TREANT]),
            make_character(id="SBB_CHARACTER_KINGTREE", position=4, attack=2, health=42,
                           golden=True, tribes=[Tribe.EVIL, Tribe.TREANT]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=5, attack=7, health=7, tribes=[Tribe.TREANT]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=6, attack=3, health=3, tribes=[Tribe.TREANT]),
            make_character(id="SBB_CHARACTER_ELDERTREANT", position=7, attack=12, health=16, golden=True,
                           tribes=[Tribe.TREANT]),
        ],
        treasures=[
            '''SBB_TREASURE_TREASURECHEST''',
            '''SBB_TREASURE_THEROUNDTABLE''',
            '''SBB_TREASURE_POWERGEM'''
        ]
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    for pos in range(1, 8):
        char = board.p1.characters[pos]
        if pos == 1:
            assert (char.attack, char.health) == (200, 200)
        elif pos == 2:
            assert (char.attack, char.health) == (122, 122)
        elif pos == 3:
            assert (char.attack, char.health) == (124, 124)
        elif pos == 4:
            assert (char.attack, char.health) == (98, 98)
        elif pos == 5:
            assert (char.attack, char.health) == (2529, 1646)
        elif pos == 6:
            assert (char.attack, char.health) == (2525, 1642)
        elif pos == 7:
            assert (char.attack, char.health) == (104, 104)
        else:
            raise ValueError('How did you get something in this position')


