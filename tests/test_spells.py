import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('spell', spell_registry.keys())
def test_spell(spell):
    player = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', attack=1, position=1, tribes=[tribe.value for tribe in Tribe])],
        spells=[spell]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=1, health=1)],
    )
    fight(player, enemy, limit=-1)


def test_falling_stars():
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1),
            make_character(position=2),
            make_character(position=3),
            make_character(position=4),
            make_character(position=5),
            make_character(position=6),
            make_character(position=7),

        ],
        spells=['''SBB_SPELL_FALLINGSTARS''', ]
    )
    enemy = make_player(raw=True)
    fight(player, enemy, limit=-1)

    for pos in range(1, 8):
        assert player.characters[pos] is None

    for char in player.graveyard:
        assert char._action_history[0].reason == ActionReason.FALLING_STARS, char._action_history[0]

    assert len(player.graveyard) == 7


@pytest.mark.parametrize('repeat', range(30))
def test_lightning_bolt(repeat):
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_LIGHTNINGBOLT''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=10),
            make_character(position=1, attack=1, health=10)
        ],
    )
    fight(player, enemy, limit=-1)

    assert enemy.characters[5] is None
    assert enemy.characters[1] is not None

    char = enemy.graveyard[0]
    assert char._action_history[0].reason == ActionReason.LIGHTNING_BOLT, char._action_history[0]


def test_fire_ball():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_FIREBALL''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=2, health=4),
            make_character(position=5, health=4),
            make_character(position=6, health=5),
            make_character(position=7),
        ],
    )
    fight(player, enemy, limit=-1)

    for char in enemy.graveyard:
        char._action_history[0].reason = ActionReason.FIREBALL
    
    # TODO make sure we do correct death ordering
    # char = enemy.graveyard[0]
    # assert char.position == 2
    # assert char._action_history[0].reason == StatChangeCause.FIREBALL
    #
    # char = enemy.graveyard[1]
    # assert char.position == 5
    # assert char._action_history[0].reason == StatChangeCause.FIREBALL
    #
    # char = enemy.characters[6]
    # assert char._action_history[0].reason == StatChangeCause.FIREBALL

    for pos in [7]:
        char = enemy.characters[pos]
        assert char is not None
        assert char._damage == 0


def test_fire_ball_backline():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_FIREBALL''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=6, health=5),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.characters[6]
    assert char._action_history[0].reason == ActionReason.FIREBALL


def test_shrivel():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=4, health=13),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert char
    assert char._action_history[0].reason == ActionReason.SHRIVEL
    assert char.attack == 0 and char.health == 1


def test_shrivel_phoenixfeather():
    player = make_player(
        characters=[make_character()],
        treasures=['SBB_TREASURE_PHOENIXFEATHER']
    )
    enemy = make_player(
        raw=True,
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )

    unit = player.characters[1]
    fight(player, enemy, limit=-1)

    assert player.characters[1] is unit


@pytest.mark.parametrize('survives', (True, False))
def test_shrivel_speed(survives):
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=0, health=(13 if survives else 11)),
        ],
        treasures=[
            "SBB_TREASURE_IVORYOWL"
        ]
    )

    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert char is not None


@pytest.mark.parametrize('survives', (True, False))
def test_shrivel_speed2(survives):
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_KINGARTHUR", attack=0, health=(13 if survives else 11), golden=True,
                           tribes=[Tribe.ROYAL]),
        ],
    )

    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert char is not None


def test_spells_damaging_darkwood():
    player = make_player(
        raw=True,
        spells=[
            '''SBB_SPELL_ENFEEBLEMENT''',
            '''SBB_SPELL_FALLINGSTARS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_DARKWOODCREEPER", attack=12, health=15),
        ],
    )

    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert (char.attack, char.health) == (1, 2)


def test_multiple_spells():
    player = make_player(
        raw=True,
        spells=[
            '''SBB_SPELL_FIREBALL''',
            '''SBB_SPELL_LIGHTNINGBOLT'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=0, health=4, position=1),
            make_character(attack=0, health=14, position=5),
        ],
    )
    frontchar = enemy.characters[1]
    backchar = enemy.characters[5]
    fight(player, enemy, limit=-1)

    assert frontchar._action_history[0].reason == ActionReason.FIREBALL
    assert set([statchange.reason for statchange in backchar._action_history]) == {ActionReason.FIREBALL,
                                                                                   ActionReason.LIGHTNING_BOLT}

def test_earthquake():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_EARTHQUAKE''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1, health=2),
            make_character(position=2, health=3),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.graveyard[0]
    assert char
    assert char._action_history[0].reason == ActionReason.EARTHQUAKE

    char = enemy.characters[2]
    assert char
    assert char._action_history[0].reason == ActionReason.EARTHQUAKE
    assert char.health == 1


def test_earthquake_peeps():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_EARTHQUAKE''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1, health=1),
            make_character(id="SBB_CHARACTER_PRINCESSPEEP", position=2, ),
            make_character(position=3, health=5),
            make_character(position=4, health=5),
            make_character(position=5, health=5),
            make_character(position=6, health=5),
            make_character(position=7, health=5),

        ],
    )
    fight(player, enemy, limit=-1)

    for pos in [1, 2]:
        char = enemy.characters[pos]
        assert char.id == "SBB_CHARACTER_SHEEP"


def test_poison_apple():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_POISONAPPLE''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(health=99),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert char
    assert char._action_history[0].reason == ActionReason.POISON_APPLE
    assert char.health == 1


def test_disintegrate():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_DISINTEGRATE''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(health=30),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.graveyard[0]
    assert char
    assert char._action_history[0].reason == ActionReason.SMITE


def test_pigomorph():
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_PIGOMORPH''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert char
    assert char.id == 'SBB_CHARACTER_PIG'


@pytest.mark.parametrize('r', range(30))
def test_pigomorph_repeated(r):
    player = make_player(
        raw=True,
        spells=['''SBB_SPELL_PIGOMORPH''', '''SBB_SPELL_PIGOMORPH''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(),
            make_character(position=2),
        ],
    )
    fight(player, enemy, limit=-1)

    char = enemy.characters[1]
    assert char
    assert char.id == 'SBB_CHARACTER_PIG'

    char = enemy.characters[2]
    assert char
    assert char.id == 'SBB_CHARACTER_PIG'


def test_cats_call():
    player = make_player(
        raw=True,
        characters=[make_character()],
        spells=['''SBB_SPELL_BEASTWITHIN''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=2),
        ],
    )
    fight(player, enemy, limit=-1)

    for i in range(1, 5):
        char = player.characters[i]
        assert char
        assert char.id == 'SBB_CHARACTER_CAT'


def test_toil_and_trouble():
    player = make_player(
        raw=True,
        characters=[
            make_character(attack=0),
            make_character(position=2, attack=0),
        ],
        spells=['''SBB_SPELL_MENAGERIE''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(),
        ],
    )
    fight(player, enemy, limit=-1)

    for i in range(1, 3):
        char = player.characters[i]
        assert char
        assert char._action_history[0].reason == ActionReason.TOIL_AND_TROUBLE


@pytest.mark.parametrize('ranged', (True, False))
@pytest.mark.parametrize('one_att', (True, False))
def test_fog(ranged, one_att):
    player = make_player(
        characters=[ make_character(id="SBB_CHARACTER_FOXTAILARCHER" if ranged else '', attack=1 if one_att else 10)]
    )

    enemy = make_player(
        spells=['SBB_SPELL_FOG']
    )
    fight(player, enemy)

    character = player.characters[1]

    expected_attack = 10 if (not ranged and not one_att) else 1
    assert character.attack == expected_attack

    fogbuffs = [
        r for r in character._action_history if r.reason == ActionReason.FOG
    ]

    assert len(fogbuffs) == (1 if ranged and not one_att else 0)
    # TODO: test with singing swords
