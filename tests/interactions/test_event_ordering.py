import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('r', range(30))
def test_falling_stars_guides_eventorder(r):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=3, id='SBB_CHARACTER_GOODBOY'),
            make_character(position=2, id='SBB_CHARACTER_WRETCHEDMUMMY'),
            make_character(position=1, id='P1TESTCHAR', tribes={Tribe.GOOD}, health=2),
        ],
        spells=['''SBB_SPELL_FALLINGSTARS''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=3, id='SBB_CHARACTER_GOODBOY'),
            make_character(position=2, id='SBB_CHARACTER_WRETCHEDMUMMY'),
            make_character(position=1, id='P2TESTCHAR', tribes={Tribe.GOOD}, health=2),
        ],
    )
    fight(player, enemy, limit=0)

    livingchar = player.characters[1]
    assert livingchar, ([i.pretty_print() for i in player.valid_characters()], [i.pretty_print() for i in enemy.valid_characters()])
    assert livingchar.attack == 2
    assert livingchar.health == 1

    assert len(enemy.graveyard) == 3
