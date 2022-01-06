import pytest

from sbbbattlesim import Board
from sbbbattlesim.characters import registry as character_registry, Character
from sbbbattlesim.events import OnDamagedAndSurvived
from tests import make_character, make_player


@pytest.mark.parametrize('num_treasures', (0, 1, 2, 3))
@pytest.mark.parametrize('golden', (True, False))
def test_crafty_raw(num_treasures, golden):
    treasures = ['''SBB_TREASURE_HERMES'BOOTS''', '''SBB_TREASURE_BADMOON''', '''SBB_TREASURE_BOOKOFHEROES''']
    treasures = treasures[:num_treasures]

    fs = (4 if golden else 2) + len(treasures) * (4 if golden else 2)
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_DWARVENARTIFICER", position=1, attack=fs, health=fs, golden=golden)
        ],
        treasures=treasures
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})

    winner, loser = board.fight(limit=2)

    assert (board.p1.characters[1]._base_attack, board.p1.characters[1]._base_health) == (fs, fs)


@pytest.mark.parametrize('num_treasures', (0, 1, 2, 3))
@pytest.mark.parametrize('golden', (True, False))
def test_crafty_spawn(num_treasures, golden):
    treasures = ['''SBB_TREASURE_HERMES'BOOTS''', '''SBB_TREASURE_BADMOON''', '''SBB_TREASURE_BOOKOFHEROES''']
    treasures = treasures[:num_treasures]

    player = make_player(
        raw=True,
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
                player=self.manager.player,
                position=self.manager.position,
                golden=golden
            )
            self.manager.player.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=2)


    fs = 1 + len(treasures) * (4 if golden else 2)
    fs2 = fs + (3 if golden else 1)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (fs2, fs2)
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (fs, fs)
