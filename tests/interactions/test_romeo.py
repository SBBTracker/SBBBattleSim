import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_romeo_summons_dead_juliet(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=6, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_stats = (21, 21) if golden else (14, 14)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == final_stats
    assert board.p1.characters[6].id == juliet.id


def test_romeo_summons_dead_juliet():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=5, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_DOOMBREATH", attack=7, health=7)],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[1] is juliet

def test_romeo_doesnt_summon_anything():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[6] is None


def test_two_romeo_summons_one_dead_juliet():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=3, attack=1, health=1),
            make_character(id='SBB_CHARACTER_ROMEO', position=7, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (14, 14)
    assert board.p1.characters[3].id == juliet.id


def test_two_romeo_summons_dead_juliet_alot():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=3, attack=1, health=1),
            make_character(id='SBB_CHARACTER_ROMEO', position=7, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=50, health=50)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=4)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (21, 21)
    assert board.p1.characters[7].id == juliet.id


def test_romeo_muerte_summons_dead_juliet():
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=2, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[1]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (14, 14)
    assert board.p1.characters[2].id == juliet.id
    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (14, 14)
    assert board.p1.characters[3].id == juliet.id
