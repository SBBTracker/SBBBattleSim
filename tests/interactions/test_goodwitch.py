import pytest

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_goodwitch(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_GOODWITCHOFTHENORTH", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.GOOD]),
            make_character(position=2, attack=1, health=1)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    fight(player, enemy, limit=0)


    char = player.characters[1]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == (4 if golden else 2)
    assert healthbuffs == (6 if golden else 3)

    char = player.characters[2]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 0
    assert healthbuffs == 0


def test_goodwitch_onsummon():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_GOODWITCHOFTHENORTH", position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_PRINCESSPEEP", position=1, attack=1, health=1, tribes=[Tribe.GOOD]),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(characters=[make_character(position=5, attack=5, health=5)])
    fight(player, enemy, limit=1)

    sheep = player.characters[1]
    assert sheep.id == "SBB_CHARACTER_SHEEP"

    char = sheep
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 2
    assert healthbuffs == 3



@pytest.mark.parametrize('dies', (True, False))
def test_summon_goodwitch(dies):
    characters = [
        make_character(position=1, attack=1, health=2, tribes=[Tribe.GOOD]),
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
    donkey = player.characters[1]

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_GOODWITCHOFTHENORTH"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(5, [summon])

    donkey.register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=1 if dies else 0)

    if dies:
        assert player.characters[5] is None
    else:
        assert player.characters[5] is not None

    assert player.characters[1].health == (2 if dies else 4)
    assert player.characters[1].attack == (1 if dies else 3)
