import pytest

from sbbbattlesim import Board
from tests import make_player, make_character


@pytest.mark.parametrize('attack_postition', range(1, 8))
@pytest.mark.parametrize('defend_postition', range(1, 8))
@pytest.mark.parametrize('attack', (True, False))
def test_combat(attack_postition, defend_postition, attack):
    player = make_player(
        characters=[make_character(position=attack_postition)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else []
    )

    enemy = make_player(
        characters=[make_character(position=defend_postition)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if not attack else []
    )

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=5)


@pytest.mark.parametrize('attack', (True, False))
def test_combat_lockout(attack):
    player = make_player(
        characters=[make_character(attack=0, health=2, position=7)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else []
    )

    enemy = make_player(
        characters=[make_character(attack=2, health=2, position=7)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if not attack else []
    )

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=5)

