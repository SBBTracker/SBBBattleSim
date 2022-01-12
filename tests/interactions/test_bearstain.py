import pytest
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player
from sbbbattlesim.action import ActionReason


@pytest.mark.parametrize('golden', (True, False))
def test_bearstain_black_cat_dying(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    final_stats = (15, 15) if golden else (6, 6)
    assert board.p1.characters[1].display_name == 'Cat'
    assert board.p1.characters[1].attack, board.p1.characters[1].health == final_stats


@pytest.mark.parametrize('golden', (True, False))
def test_bearstain_black_cat_living(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', tribes=['animal'], position=1),
        ],
    )
    enemy = make_player(raw=True)
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)

    char = board.p1.characters[1]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == (4 if golden else 2)
    assert healthbuffs == (4 if golden else 2)


@pytest.mark.parametrize('golden', (True, False))
def test_two_bearstain_black_cat_dying(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=golden),
            make_character(id='SBB_CHARACTER_PROSPERO', position=6, golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    final_stats = (45, 45) if golden else (15, 15)
    assert board.p1.characters[1].display_name == 'Cat'
    assert board.p1.characters[1].attack, board.p1.characters[1].health == final_stats


@pytest.mark.parametrize('dies', (True, False))
def test_summon_bearstain(dies):
    characters = [
        make_character(position=1, attack=1, health=2, tribes=[Tribe.ANIMAL]),
    ]

    player = make_player(
        raw=True,
        level=3,
        characters=characters
    )

    enemy_characters = []
    if dies:
        enemy_characters.append(make_character(id="SBB_CHARACTER_BABYDRAGON", position=1, attack=300, health=300))

    enemy = make_player(
        raw=True,
        spells=["SBB_SPELL_FALLINGSTARS"],
        characters=enemy_characters,
        treasures = [
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    donkey = board.p1.characters[1]

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_PROSPERO"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(5, [summon])

    donkey.register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=(1 if dies else 0))


    bearstain = board.p1.characters[5]
    if dies:
        assert bearstain is None, bearstain.pretty_print()
        assert (donkey.attack, donkey.health) == (1, 2)
    else:
        assert (bearstain.attack, bearstain.health) == (bearstain._attack, bearstain._health)
        assert (donkey.attack, donkey.health) == (3, 3)