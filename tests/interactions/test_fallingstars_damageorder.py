import pytest

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_angry_fallingstars():
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_DWARFMINER", position=1, attack=1, health=2, tribes=[Tribe.DWARF]
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.DWARF]),
        ],
    )
    enemy = make_player(
        spells=["SBB_SPELL_FALLINGSTARS"]
    )
    fight(player, enemy, limit=2)


    assert (player.characters[6].attack, player.characters[6].health) == (3, 2)


def test_donkey_fallingstars():
    player = make_player(
        characters=[
            make_character(position=1, attack=1, health=2),
            make_character(position=2, attack=1, health=2),
            make_character(position=3, attack=1, health=2),
            make_character(position=4, attack=1, health=2),
            make_character(position=6, attack=1, health=2),
            make_character(position=7, attack=1, health=2),
        ],
    )
    enemy = make_player(
        spells=["SBB_SPELL_FALLINGSTARS"]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_DARKWOODCREEPER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[3].register(FakeTrojanDonkeySummon)
    fight(player, enemy, limit=2)

    for pos in range(1, 8):
        char = player.characters[pos]
        if pos <= 3:
            assert char.attack == 1, pos
            assert char.health == 1, pos
        elif pos == 5:
            assert char.attack == 0
            assert char.health == 3
        else:
            assert char.attack == 2
            assert char.health == 1


@pytest.mark.parametrize('board_full', (True, False))
def test_donkey_fallingstars_fullboard(board_full):
    characters = [
        make_character(position=2, attack=1, health=1),
        make_character(position=3, attack=1, health=1),
        make_character(id="SBB_CHARACTER_TROJANDONKEY", position=4, attack=1, health=2),
        make_character(position=5, attack=1, health=1),
        make_character(position=6, attack=1, health=1),
        make_character(position=7, attack=1, health=1),
    ]
    if board_full:
        characters.append(make_character(position=1, attack=1, health=1))

    player = make_player(
        level=3,
        characters=characters
    )
    enemy = make_player(
        spells=["SBB_SPELL_FALLINGSTARS"]
    )
    donkey = player.characters[4]

    fight(player, enemy, limit=0)

    for pos in range(1, 8):
        char = player.characters[pos]
        if not board_full:
            if pos == 1:
                assert char is not None
                assert char._damage == 0
            elif pos == 4:
                assert char is donkey
            else:
                assert char is None
        else:
            if pos == 4:
                assert char is donkey
            else:
                assert char is None


def test_donkey_fallingstars_summondragon():
    player = make_player(
        characters=[
            make_character(position=1, attack=0, health=2),
        ],
    )
    enemy = make_player(
        characters=[
            make_character(health=5)
        ],
        spells=["SBB_SPELL_FALLINGSTARS"]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_LIGHTNINGDRAGON"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)
    fight(player, enemy, limit=0)

    assert enemy.characters[1] is None
    assert player.graveyard[0]._action_history[-1].source == enemy.graveyard[0]

