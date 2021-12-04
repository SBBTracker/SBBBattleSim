from sbbbattlesim import Board
from sbbbattlesim.characters import Character
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
import pytest


@pytest.mark.parametrize('num_treasures', (0, 1, 2, 3))
@pytest.mark.parametrize('golden', (True, False))
def test_crafty_spawn(num_treasures, golden):
    treasures = ['''SBB_TREASURE_HERMES'BOOTS''', '''SBB_TREASURE_BADMOON''', '''SBB_TREASURE_BOOKOFHEROES''']
    treasures = treasures[:num_treasures]

    player = make_player(
        characters=[
            make_character(position=1, attack=1, health=2),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=2),
        ],
        treasures=treasures
    )
    enemy = make_player(
        spells=["SBB_SPELL_FALLINGSTARS"]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_DWARVENARTIFICER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=golden
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    fs = 1 + len(treasures)*(6 if golden else 3)
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (fs, fs)


