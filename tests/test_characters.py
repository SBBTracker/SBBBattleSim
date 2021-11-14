import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe, StatChangeCause
from tests import make_character, make_player, get_characters


@pytest.mark.parametrize('attack', (True, False))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters())
def test_character(char, attack, golden):
    char = make_character(id=char, golden=golden)
    generic_char = make_character(position=7, tribes=[tribe.value for tribe in Tribe])
    player = make_player(
        characters=[char, generic_char],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else []
    )
    enemy = make_player(
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if not attack else []
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=5)


SUPPORT_EXCLUSION = (
    'SBB_CHARACTER_RIVERWISHMERMAID',
    'SBB_CHARACTER_ELDERTREANT',
    'SBB_CHARACTER_BABAYAGA'
)

@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.support is True))
def test_support(char, golden):
    support = make_character(id=char, position=5, golden=golden)
    generic_char = make_character(tribes=[tribe.value for tribe in Tribe])
    player = make_player(
        characters=[support, generic_char],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=50, health=50)],
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
    slay = make_character(id=char, position=1, golden=golden)
    player = make_player(
        characters=[slay],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(position=i) for i in range(1, 5)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.last_breath is True))
def test_last_breath(char, golden):
    last_breath = make_character(id=char, position=1, attack=0, health=1, golden=golden)
    player = make_player(
        characters=[last_breath],
    )
    enemy = make_player(
        characters=[make_character(attack=50, health=50)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()


@pytest.mark.parametrize('golden', (True, False))
def test_baba_yaga(golden):
    lance = make_character(id='SBB_CHARACTER_LANCELOT', position=1, attack=1, health=1)
    baba = make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=0, health=1, golden=golden)
    player = make_player(
        characters=[lance, baba],
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    if golden:
        assert player.characters[1].attack == 7
    else:
        assert player.characters[1].attack == 5


def test_soltak():
    soltak = make_character(id='SBB_CHARACTER_SOLTAKANCIENT', position=1, attack=0, health=1)
    generic = make_character(id='GENERIC', attack=1, health=1, position=5)
    player = make_player(
        characters=[soltak, generic],
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_BABYDRAGON', health=2)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    assert player.characters[5] is None and winner is player
