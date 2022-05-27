import pytest

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
from tests import make_character, make_player


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
    fight(player, enemy, limit=1)

    if summoner_id == 'SBB_CHARACTER_PRINCESSPEEP':
        if golden:
            final_stats = (1, 13)
        else:
            final_stats = (1, 7)
    else:
        final_stats = (1, 1)
        assert player.characters[1] is not None  # there should be a tweedle dum there

    assert (player.characters[5].attack, player.characters[5].health) == final_stats


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
    donkey = player.characters[1]

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_HUNGRYHUNGRYHIPPOCAMPUS"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    donkey.register(FakeTrojanDonkeySummon)
    donkey.register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=0)

    hippocampus1 = player.characters[2]
    assert (hippocampus1.attack, hippocampus1.health) == (hippocampus1._attack, hippocampus1._health+2)

    hippocampus2 = player.characters[3]
    assert (hippocampus2.attack, hippocampus2.health) == (hippocampus2._attack, hippocampus2._health)
