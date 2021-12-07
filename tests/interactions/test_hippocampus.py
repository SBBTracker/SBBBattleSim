import pytest

from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe
from sbbbattlesim.characters import registry as character_registry


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('summoner_id', ('SBB_CHARACTER_PRINCESSPEEP', 'SBB_CHARACTER_TWEEDLEDEE'))
def test_hippocampus(golden, summoner_id):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_HUNGRYHUNGRYHIPPOCAMPUS", position=5, attack=1, health=1, golden=golden),
            make_character(id=summoner_id, position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if summoner_id == 'SBB_CHARACTER_PRINCESSPEEP':
        if golden:
            final_stats = (1, 13)
        else:
            final_stats = (1, 7)
    else:
        final_stats = (1, 1)
        assert board.p1.characters[1] is not None  # there should be a tweedle dum there

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == final_stats


def test_summon_hippocampus():
    characters = [
        make_character(position=1, attack=1, health=2),
    ]

    player = make_player(
        level=3,
        characters=characters
    )
    enemy = make_player(
        spells=["SBB_SPELL_FALLINGSTARS"]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    donkey = board.p1.characters[1]

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_HUNGRYHUNGRYHIPPOCAMPUS"].new(
                owner=self.manager.owner,
                position=self.manager.position,
                golden=False
            )
            self.manager.owner.summon(self.manager.position, [summon])

    donkey.register(FakeTrojanDonkeySummon)
    donkey.register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    hippocampus1 = board.p1.characters[2]
    assert (hippocampus1.attack, hippocampus1.health) == (hippocampus1._attack, hippocampus1._health+2)

    hippocampus2 = board.p1.characters[3]
    assert (hippocampus2.attack, hippocampus2.health) == (hippocampus2._attack, hippocampus2._health)
