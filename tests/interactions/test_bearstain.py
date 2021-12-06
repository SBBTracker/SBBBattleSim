import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_bearstain_black_cat_dying(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_stats = (15, 15) if golden else (6, 6)
    assert board.p1.characters[1].display_name == 'Cat'
    assert board.p1.characters[1].attack, board.p1.characters[1].health == final_stats


@pytest.mark.parametrize('golden', (True, False))
def test_bearstain_black_cat_living(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_stats = (5, 5) if golden else (3, 3)
    assert board.p1.characters[1].attack, board.p1.characters[1].health == final_stats


@pytest.mark.parametrize('golden', (True, False))
def test_two_bearstain_black_cat_dying(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=golden),
            make_character(id='SBB_CHARACTER_PROSPERO', position=6, golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_stats = (45, 45) if golden else (15, 15)
    assert board.p1.characters[1].display_name == 'Cat'
    assert board.p1.characters[1].attack, board.p1.characters[1].health == final_stats
