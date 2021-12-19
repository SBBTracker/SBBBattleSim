import pytest

from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.characters import registry as character_registry

@pytest.mark.parametrize('golden', (True, False))
def test_baby_root(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    if golden:
        final_stats = (1, 7)
    else:
        final_stats = (1, 4)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == final_stats


@pytest.mark.parametrize('dies', (True, False))
def test_summon_babyroot(dies):
    characters = [
        make_character(position=1, attack=1, health=2),
        make_character(position=2, attack=1, health=2),
        make_character(position=3, attack=1, health=2),
        make_character(position=4, attack=1, health=2),
    ]

    player = make_player(
        level=3,
        characters=characters
    )

    enemy_characters = []
    if dies:
        enemy_characters.append(make_character(id="SBB_CHARACTER_BABYDRAGON", position=1, attack=300, health=300))

    enemy = make_player(
        spells=["SBB_SPELL_FALLINGSTARS"],
        characters=enemy_characters,
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    donkey = board.p1.characters[1]

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_BABYROOT"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(5, [summon])

    donkey.register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1 if dies else 0)

    if dies:
        assert board.p1.characters[5] is None
    else:
        assert board.p1.characters[5] is not None

    assert board.p1.characters[1].health == (2 if dies else 4)
