import pytest

from sbbbattlesim import Board
from tests import make_character, make_player

def test_onstart_not_proc_merlin():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1)
        ],
        hero='SBB_HERO_MERLIN',
        spells=[
            'SBB_SPELL_EARTHQUAKE'
        ]
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.attack == 1 and generic.health == 1


def test_onstart_not_proc_familar():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_WIZARD', position=1)
        ],
        spells=[
            'SBB_SPELL_EARTHQUAKE'
        ]
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    cat = player.characters.get(1)

    assert cat
    assert cat.attack == 1 and cat.health == 1