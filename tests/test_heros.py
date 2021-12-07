import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe
from tests import make_character, make_player


def test_charon():
    player = make_player(
        characters=[
            make_character(id='TEST', position=1),
            make_character(position=5)
        ],
        hero='SBB_HERO_CHARON'
    )
    enemy = make_player(
        characters=[
            make_character(id='TEST', position=1),
            make_character(position=5)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    dead = player.graveyard[0]
    assert dead
    assert dead.attack == 3 and dead.health + dead._damage == 2

    also_dead = player.graveyard[1]
    assert also_dead
    assert also_dead.attack == 1 and also_dead.health + dead._damage == 1


@pytest.mark.parametrize('on', (True, False))
@pytest.mark.parametrize('evil_back', (True, False))
def test_evella(on, evil_back):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, tribes=['animal', 'evil'] if on else []),
            make_character(id='EVIL', position=5, tribes=['evil'] if evil_back else [])
        ],
        hero='SBB_HERO_DARKONE'
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    buffed_animal = player.characters.get(5)
    buffed_cat = player.characters.get(1)

    assert buffed_animal
    assert buffed_animal.attack == (2 if on and evil_back else 1) and buffed_animal.health == 1
    assert buffed_cat
    assert buffed_cat.attack == (2 if on else 1) and buffed_cat.health == 1


@pytest.mark.parametrize('on', (True, False))
def test_sad_dracula(on):
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1 if on else 2),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=5)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        hero='SBB_HERO_DRACULA'
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    shadow_assassin = player.characters.get(5)

    assert shadow_assassin
    assert shadow_assassin.attack == (2 if on else 1) and shadow_assassin.health == (2 if on else 1)


@pytest.mark.parametrize('on', (True, False))
def test_fate(on):
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1, golden=on),
        ],
        hero='SBB_HERO_FATE'
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.attack == (6 if on else 1) and generic.health == (6 if on else 1)


def test_gepetto():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
        hero='SBB_HERO_GEPETTO',
        level=3
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    cat = player.characters.get(1)

    assert cat
    assert cat.attack == 4 and cat.health == 4


@pytest.mark.parametrize('on', (True, False))
def test_krampus(on):
    player = make_player(
        characters=[
            make_character(id='EVIL', position=1, tribes=['evil'] if on else []),
        ],
        hero='SBB_HERO_KRAMPUS',
        level=3
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    evil = player.characters.get(1)

    assert evil
    assert evil.attack, evil.health == ((2, 2) if on else (1, 1))


@pytest.mark.parametrize('on', (True, False))
def test_mrsclaus(on):
    player = make_player(
        characters=[
            make_character(id='GOOD', position=1, tribes=['good'] if on else []),
        ],
        hero='SBB_HERO_MRSCLAUS',
        level=3
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    good = player.characters.get(1)

    assert good
    assert good.attack, good.health == ((2, 2) if on else (1, 1))


def test_merlin():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MONSTERBOOK'),
            make_character(attack=0, position=7)
        ],
        hero='SBB_HERO_MERLIN',
        level=6
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    char = player.characters.get(7)

    assert char
    assert char.attack == 2 and char.health == 2


@pytest.mark.parametrize('on', (True, False))
def test_jacks_giant(on):
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1 if on else 5)
        ],
        hero='SBB_HERO_SIRPIPS-A-LOT',
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    generic = player.characters.get(1 if on else 5)

    assert generic
    assert generic.health == (3 if on else 1)


@pytest.mark.parametrize('on', (True, False))
def test_mirhi(on):
    player = make_player(
        characters=[
            make_character(id='ROYAL', position=1, tribes=['prince'] if on else []),
            make_character(id='ROYAL', position=2, tribes=['princess'] if on else [])
        ],
        hero='SBB_HERO_KINGLION',
        mirhi_buff=5
    )

    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    for pos in [1, 2]:
        royal = player.characters.get(pos)

        assert royal
        assert royal.attack == (6 if on else 1) and royal.health == (11 if on else 1)


def test_trophy_hunter():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].id == 'Cat'
    assert player.characters[2].id == 'Cat'

def test_trophy_hunter():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_CLOAKOFTHEASSASSIN''']
    )

    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert (player.characters[1].attack, player.characters[1].health) == (4, 4)


def test_trophy_hunter_yaga():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
            make_character(id="SBB_CHARACTER_BABAYAGA", position=5)
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
    )

    enemy = make_player(
        characters=[
            make_character()
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    for pos in [1, 2, 3]:
        assert player.characters[pos].id == "SBB_CHARACTER_CAT"


@pytest.mark.parametrize('limit', (1, 3, 5))
def test_trophy_hunter_friendlyspirit(limit):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FRIENDLYGHOST', position=1, attack=5, health=10),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        hero='SBB_HERO_MILITARYLEADER',
    )

    enemy = make_player(
        characters=[
            make_character(attack=0, position=1),
            make_character(attack=0, position=2),
            make_character(attack=0, position=3),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=limit)
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    ghost = board.p1.characters[1]
    if limit == 1:
        final_stats = (10, 20)
    elif limit == 3:
        final_stats = (20, 40)
    elif limit == 5:
        final_stats = (40, 80)
    else:
        raise ValueError(f'Limit of {limit} is not configured in the test')

    assert (ghost.attack, ghost.health) == final_stats


# def test_modred():
#     player = make_player(
#         characters=[
#             make_character()
#         ],
#         hero='SBB_HERO_MORDRED',
#         hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
#     )
#
#     enemy = make_player(
#         characters=[make_character(id='GENERIC', position=1)],
#     )
#     board = Board({'PLAYER': player, 'ENEMY': enemy})
#     winner, loser = board.fight()
#     board.p1.resolve_board()
#     board.p2.resolve_board()
#
#     player = board.p1
#
#     assert player.characters[1].id == 'TEST3'


@pytest.mark.parametrize('on', (True, False))
def test_beauty(on):
    player = make_player(
        characters=[
            make_character(position=1, tribes=['good'] if on else []),
            make_character(position=2, tribes=['evil'] if on else [])
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    t1 = player.characters[1].tribes
    t2 = player.characters[2].tribes
    tribe_set = {Tribe.EVIL, Tribe.GOOD}
    assert t1 == tribe_set if on else t1 == set()
    assert t2 == tribe_set if on else t2 == set()


@pytest.mark.parametrize('treasure', ("SBB_TREASURE_CORRUPTEDHEARTWOOD", "SBB_TREASURE_CROWNOFATLAS"))
def test_beauty_withtreasure(treasure):
    player = make_player(
        characters=[
            make_character(position=1, tribes=[Tribe.ANIMAL]),
        ],
        treasures=[
            treasure
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].tribes == {Tribe.GOOD, Tribe.EVIL, Tribe.ANIMAL}


def test_beauty_spawnedanimal():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=1, ),
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player(
        characters=[
            make_character()
        ]
    )

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].tribes == {Tribe.GOOD, Tribe.EVIL, Tribe.ANIMAL}

FALLEN_ANGEL_TESTS = (
    (['good'], 1, 3),
    (['evil'], 3, 1),
    (['good', 'evil'], 3, 3),
    ([], 1, 1)
)

@pytest.mark.parametrize('tribes, attack, health', FALLEN_ANGEL_TESTS)
def test_fallen_angel(tribes, attack, health):
    player = make_player(
        characters=[make_character(position=i, tribes=tribes) for i in range(1, 4)],
        hero='SBB_HERO_FALLENANGEL',
    )

    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    for char in player.characters.values():
        if char:
            assert char.health == health
            assert char.attack == attack


def test_muerte():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MUERTE',
    )

    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].id == 'SBB_CHARACTER_CAT'
    assert player.characters[2].id == 'SBB_CHARACTER_CAT'
