import pytest

from sbbbattlesim import Board
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.utils import Keyword, Tribe, StatChangeCause
from tests import make_character, make_player


@pytest.mark.parametrize('spell', spell_registry.keys())
def test_spell(spell):
    player = make_player(
        characters=[make_character(id='GENERIC', attack=1, position=1, keywords=[kw.value for kw in Keyword],
                                   tribes=[tribe.value for tribe in Tribe])],
        spells=[spell]
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)


def test_falling_stars():
    player = make_player(
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
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    for pos in range(1, 8):
        assert board.p1.characters[pos] is None

    for char in board.p1.graveyard:
        assert char.stat_history[0].reason == StatChangeCause.FALLING_STARS

    assert len(board.p1.graveyard) == 7


@pytest.mark.parametrize('repeat', range(30))
def test_lightning_bolt(repeat):
    player = make_player(
        spells=['''SBB_SPELL_LIGHTNINGBOLT''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=10),
            make_character(position=1, attack=1, health=10)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    board.p1.characters[5] is None
    board.p1.characters[1] is not None

    char = board.p2.graveyard[0]
    assert char.stat_history[0].reason == StatChangeCause.LIGHTNING_BOLT


def test_fire_ball():
    player = make_player(
        spells=['''SBB_SPELL_FIREBALL''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=2, health=4),
            make_character(position=5, health=4),
            make_character(position=6, health=5),
            make_character(position=7),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char.position == 2
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL

    char = board.p2.graveyard[1]
    assert char.position == 5
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL

    char = board.p2.characters[6]
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL

    for pos in [7]:
        char = board.p2.characters[pos]
        assert char is not None
        assert char._damage == 0


def test_fire_ball_backline():
    player = make_player(
        spells=['''SBB_SPELL_FIREBALL''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=6, health=5),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.characters[6]
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL


def test_shrivel():
    player = make_player(
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=4, health=13),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    char = board.p2.characters[1]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.SHRIVEL
    assert char.attack == 0 and char.health == 1


@pytest.mark.parametrize('survives', (True, False))
def test_shrivel_speed(survives):
    player = make_player(
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=(13 if survives else 11)),
        ],
        treasures=[
            "SBB_TREASURE_IVORYOWL"
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    char = board.p2.characters[1]
    if survives:
        assert char is not None
    else:
        assert char is None


@pytest.mark.parametrize('survives', (True, False))
def test_shrivel_speed2(survives):
    player = make_player(
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_KINGARTHUR", attack=0, health=(13 if survives else 11), golden=True,
                           tribes=[Tribe.PRINCE]),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    char = board.p2.characters[1]
    if survives:
        assert char is not None
    else:
        assert char is None


def test_spells_damaging_darkwood():
    player = make_player(
        spells=[
            '''SBB_SPELL_ENFEEBLEMENT''',
            '''SBB_SPELL_FALLINGSTARS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_DARKWOODCREEPER", attack=12, health=15),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    char = board.p2.characters[1]
    assert (char.attack, char.health) == (1, 2)


def test_multiple_spells():
    player = make_player(
        spells=[
            '''SBB_SPELL_FIREBALL''',
            '''SBB_SPELL_LIGHTNINGBOLT'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=4, position=1),
            make_character(attack=0, health=14, position=5),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    frontchar = board.p2.characters[1]
    backchar = board.p2.characters[5]
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert frontchar.stat_history[0].reason == StatChangeCause.FIREBALL
    assert set([statchange.reason for statchange in backchar.stat_history]) == {StatChangeCause.FIREBALL,
                                                                                StatChangeCause.LIGHTNING_BOLT}


def test_earthquake():
    player = make_player(
        spells=['''SBB_SPELL_EARTHQUAKE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=1, health=2),
            make_character(position=2, health=3),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.EARTHQUAKE

    char = board.p2.characters[2]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.EARTHQUAKE
    assert char.health == 1


def test_earthquake_peeps():
    player = make_player(
        spells=['''SBB_SPELL_EARTHQUAKE''', ]
    )
    enemy = make_player(
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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    for pos in [1, 2]:
        char = board.p2.characters[pos]
        assert char.id == "SBB_CHARACTER_SHEEP"


def test_poison_apple():
    player = make_player(
        spells=['''SBB_SPELL_POISONAPPLE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(health=99),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.characters[1]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.POISON_APPLE
    assert char.health == 1


def test_disintegrate():
    player = make_player(
        spells=['''SBB_SPELL_DISINTEGRATE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(health=30),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.SMITE


def test_pigomorph():
    player = make_player(
        spells=['''SBB_SPELL_PIGOMORPH''', ]
    )
    enemy = make_player(
        characters=[
            make_character(),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.characters[1]
    assert char
    assert char.id == 'SBB_CHARACTER_PIG'


def test_cats_call():
    player = make_player(
        characters=[make_character()],
        spells=['''SBB_SPELL_BEASTWITHIN''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=2),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    for i in range(1, 5):
        char = board.p1.characters[i]
        assert char
        assert char.id == 'SBB_CHARACTER_CAT'


def test_toil_and_trouble():
    player = make_player(
        characters=[
            make_character(attack=0),
            make_character(position=2, attack=0),
        ],
        spells=['''SBB_SPELL_MENAGERIE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    for i in range(1, 3):
        char = board.p1.characters[i]
        assert char
        assert char.stat_history[0].reason == StatChangeCause.TOIL_AND_TROUBLE
