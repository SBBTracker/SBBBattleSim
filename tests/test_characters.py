import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe
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


# @pytest.mark.parametrize('golden', (True, False))
# @pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.support is True))
# def test_support(char, golden):
#     front = make_character(id='TEST', attack=1, health=1, position=1)
#     support = make_character(id=char, golden=golden, position=5)
#     player = make_player([front, support], treasures=['''SBB_TREASURE_HERMES'BOOTS'''])
#     board = fight_monstar(player)
#
#     board.fight(limit=-1)
#
#     assert board.p1.characters[1].stat_history



#
# @pytest.mark.parametrize('golden', (True, False))
# @pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.slay is True))
# def test_slay(char, attack, golden):
#     char = make_character(id=char, golden=golden)
#     player = make_player([char], treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else [])
#     fight_monstar(player)
#
#
# @pytest.mark.parametrize('golden', (True, False))
# @pytest.mark.parametrize('char', get_characters(_lambda=lambda char: char.last_breath is True))
# def test_last_breath(char, attack, golden):
#     char = make_character(id=char, golden=golden)
#     player = make_player([char], treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else [])
#     fight_monstar(player)