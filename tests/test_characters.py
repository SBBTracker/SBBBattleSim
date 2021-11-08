import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe, StatChangeCause
from tests import make_character, make_player, get_characters


@pytest.mark.parametrize('attack', (True, False))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters())
def test_character(char, attack, golden):
    char = make_character(id=char, position=1, golden=golden)
    generic_char = make_character(id='GENERIC', attack=0, position=7, keywords=[kw for kw in Keyword], tribes=[tribe for tribe in Tribe])
    player = make_player(
        characters=[char, generic_char],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else []
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=50, health=50)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if not attack else []
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

SUPPORT_EXCLUSION = (
    'SBB_CHARACTER_RIVERWISHMERMAID',
    'SBB_CHARACTER_ELDERTREANT'
)

@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.support is True))
def test_support(char, golden):
    support = make_character(id=char, position=5, golden=golden)
    generic_char = make_character(id='GENERIC', attack=1, position=1, keywords=[kw for kw in Keyword], tribes=[tribe for tribe in Tribe])
    player = make_player(
        characters=[support, generic_char],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=50, health=50)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    # Riverwish is a support but doesn't give stats so it won't be tested here
    if char in SUPPORT_EXCLUSION:
        return

    assert board.p1.characters[1].stat_history[0].reason[0] == StatChangeCause.SUPPORT_BUFF


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.slay is True))
def test_slay(char, golden):
    slay = make_character(id=char, position=1, attack=1, health=1, golden=golden)
    player = make_player(
        characters=[slay],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=i, attack=0, health=1) for i in range(4)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.last_breath is True))
def test_last_breath(char, golden):
    last_breath = make_character(id=char, position=1, attack=0, health=1, golden=golden)
    player = make_player(
        characters=[last_breath],
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=i, attack=50, health=50) for i in range(4)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)